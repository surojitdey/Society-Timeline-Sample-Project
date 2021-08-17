import json
from json import JSONEncoder
import asyncio

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.hashers import make_password, check_password
from django.conf import settings

from rest_framework import viewsets, status, permissions
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.parsers import JSONParser
from rest_framework.request import Request
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.views import APIView

from users.models import User, FamilyDetails, OTP
from users.serializers import UserSerializer, FamilySerializer, userStatusSerializer, getUserSerializer, getUserByMobileNumberSerializer, forgotPasswordSerializer, UpdatePasswordSerializer, GetUserSerializer
from service_auth.permissions import IsUser, IsUserReadOnly, IsAdminUser
from helpers.otp import generate_otp, verify_otp, send_sms, create_otp, get_message_template, approved_account_message


class UserStatusUpdateViewset(viewsets.ViewSet):
  queryset = User.objects.all()
  serializer_class = userStatusSerializer
  permission_classes = [IsAdminUser]
  
  def create(self, request):
    user = User.objects.get(id=self.request.data['user_id'])
    if(self.request.data['status'] == 'active'):
      user.is_active = True
      user.save()
      approved_account_message(user.mobile_number)
      return Response("User activated.", status=status.HTTP_200_OK)
    else:
      user.is_active = False
      user.save()
      return Response("User deactivated.", status=status.HTTP_200_OK)


class GetUserViewset(viewsets.ModelViewSet):
  queryset = User.objects.all()
  serializer_class = UserSerializer
  permission_classes = [IsUser | IsAdminUser]

  def get_queryset(self):
    return User.objects.filter(mobile_number=self.request.user)


class GetAllUserViewset(viewsets.ModelViewSet):
  queryset = User.objects.all()
  serializer_class = GetUserSerializer
  permission_classes = [IsUser | IsAdminUser]

  def get_queryset(self):
    return User.objects.exclude(role=User.Role.ADMIN)


class GetApprovedUserViewset(viewsets.ModelViewSet):
  queryset = User.objects.all()
  serializer_class = UserSerializer
  permission_classes = [AllowAny]

  def get_queryset(self):
    return User.objects.exclude(role=User.Role.ADMIN).filter(is_active=True)


class UserViewset(viewsets.ModelViewSet):
  queryset = User.objects.all()
  serializer_class = UserSerializer
  permission_classes = [IsUser | IsAdminUser]

  def get_permissions(self):
    if self.request.method == 'POST':
      self.permission_classes = (AllowAny,)
    elif self.request.method == 'PUT':
      self.permission_classes = [IsUser | IsAdminUser]
    elif self.request.method == 'PATCH':
      self.permission_classes = [IsUser | IsAdminUser]
    elif self.request.method == 'GET':
      self.permission_classes = [IsAdminUser]
    
    return super(UserViewset, self).get_permissions()
  
  def get_queryset(self):
    return User.objects.all()
  
  def create(self, request):
    if 'mobile_number' in request.data:
      user = User.objects.filter(mobile_number=request.data['mobile_number'])
      if user:
        return Response({'error': 'Mobile number exits.'}, status=status.HTTP_409_CONFLICT)
    serializer = self.serializer_class(data=request.data)
    if serializer.is_valid():
      if 'password' not in serializer.validated_data:
        return Response({'error': 'Password required'}, status=status.HTTP_400_BAD_REQUEST)
      else:
        otp_obj = OTP.objects.filter(user=serializer.validated_data.get(
            'mobile_number'), otp_type=OTP.Type.SIGNUP).first()
        if otp_obj:
          if otp_obj.matched:
            user = User.objects.create_user(**serializer.validated_data)
            otp_obj.delete()
            return Response({'status' : True, 'user': user.id}, status=status.HTTP_201_CREATED)
          else:
            return Response({
                'status': False,
                'matched_failed': True,
                'detail': 'OTP does not matched.'
            }, status=status.HTTP_200_OK)
        else:
          create_otp(serializer.validated_data['mobile_number'], self.request.data,
                     settings.SIGNUP_TEMPLATE, OTP.Type.SIGNUP, user=serializer.data)
          return Response({
              'otp': True,
              'status': True,
              'detail': 'OTP created'
          }, status=status.HTTP_200_OK)
    return Response({ 'error': 'Some field is missing' }, status=status.HTTP_400_BAD_REQUEST)
  
  def perform_create(self, serializer):
    if 'password' in self.request.data:
      password = make_password(self.request.data['password'])
      serializer.save(password=password)
    else:
      serializer.save()
      

class UpdateUserViewset(viewsets.ViewSet):
  queryset = User.objects.all()
  serializer_class = UserSerializer
  permission_classes = [IsUser | IsAdminUser]

  def create(self, request):
    user = self.request.user
    if user:
      serializer = self.serializer_class(data=self.request.data, instance=user, partial=True)
      if serializer.is_valid():
        if self.request.data.get('mobile_number') == user.mobile_number:
          serializer.update(validated_data=self.request.data, instance=user)
          return Response({
            'status' : True,
            'detail' : 'User data updated.'
          }, status=status.HTTP_200_OK)
        else:
          otp_obj = OTP.objects.filter(user=self.request.data.get('mobile_number'), otp_type=OTP.Type.NUMBER_CHANGE).first()
          if otp_obj:
            if otp_obj.matched:
              serializer.update(validated_data=otp_obj.data, instance=user)
              otp_obj.delete()
              return Response({
                  'status': True,
                  'detail': 'User data updated.'
              }, status=status.HTTP_200_OK)
            else:
              return Response({
                  'status': False,
                  'matched_failed': True,
                  'detail': 'OTP does not matched.'
              }, status=status.HTTP_200_OK)
          else:
            create_otp(self.request.data['mobile_number'], self.request.data, settings.NUMBER_CHANGE_TEMPLATE, OTP.Type.NUMBER_CHANGE, user=user)
            return Response({
                'otp': True,
                'status': True,
                'detail': 'OTP created'
            }, status=status.HTTP_200_OK)
      else:
        return Response({
          'status' : False,
          'detail' : 'Some fields are missing.',
          'errors' : serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    else:
      return Response({
        'status' : False,
        'detail' : 'User not found.'
      }, status=status.HTTP_404_NOT_FOUND)


class UpdatePasswordViewset(viewsets.ViewSet):
  queryset = User.objects.all()
  serializer_class = UpdatePasswordSerializer
  permission_classes = [IsUser | IsAdminUser]

  def create(self, request):
    user = User.objects.filter(mobile_number=self.request.user).first()
    if(user):
      otp_obj = OTP.objects.filter(user=user.mobile_number, otp_type=OTP.Type.PASSWORD).first()
      if user.is_superuser:
        if 'password' in self.request.data and self.request.user.check_password(self.request.data['password']):
            password = make_password(self.request.data['new_password'])
            user.password = password
            user.save()
            return Response("Password changed", status=status.HTTP_200_OK)
        else:
          return Response("Missing fields", status=status.HTTP_400_BAD_REQUEST)
      elif otp_obj:
        if otp_obj.matched:
          if 'password' in otp_obj.data and self.request.user.check_password(otp_obj.data['password']):
            password = make_password(otp_obj.data['new_password'])
            user.password = password
            user.save()
            otp_obj.delete()
            return Response("Password changed", status=status.HTTP_200_OK)
          else:
            return Response("Missing fields", status=status.HTTP_400_BAD_REQUEST)
        else:
          return Response({
            'status' : False,
            'matched_failed' : True,
            'detail' : 'OTP does not matched'
          }, status=status.HTTP_200_OK)
      else:
        create_otp(user.mobile_number, self.request.data,
                   settings.PASSWORD_TEMPLATE, OTP.Type.PASSWORD, user=user)
        return Response({
          'otp' : True,
          'status' : True,
          'detail' : 'OTP created.'
        }, status=status.HTTP_200_OK)
    else:
      return Response("User not found", status=status.HTTP_404_NOT_FOUND)



class AdminUserViewset(viewsets.ModelViewSet):
  queryset = User.objects.all()
  serializer_class = UserSerializer
  permission_classes = [IsAdminUser]

  def get_permissions(self):
    if self.request.method == 'POST':
      self.permission_classes = (AllowAny,)
    
    return super(UserViewset, self).get_permissions()
  
  def create(self, request):
    serializer = self.serializer_class(data=request.data)
    if serializer.is_valid():
      if 'password' not in serializer.validated_data:
        return Response({'error': 'Password required'}, status=status.HTTP_400_BAD_REQUEST)
      user = User.objects.create_superuser(**serializer.validated_data)

      return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
    return Response({ 'error': 'Some field is missing' }, status=status.HTTP_400_BAD_REQUEST)
  
  def perform_create(self, serializer):
    if 'password' in self.request.data:
      password = make_password(self.request.data['password'])
      serializer.save(password=password)
    else:
      serializer.save()
      
  def perform_update(self, serializer):
    if 'password' in self.request.data:
      password = make_password(self.request.data['password'])
      serializer.save(password=password)
    else:
      serializer.save()


class FamilyViewset(viewsets.ModelViewSet):
  queryset = FamilyDetails.objects.all()
  serializer_class = FamilySerializer
  permission_classes = [AllowAny]

  def get_queryset(self):
    return FamilyDetails.objects.filter(user_id=self.request.user.id)

  def create(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data, many=isinstance(request.data, list))
    serializer.is_valid(raise_exception=True)
    self.perform_create(serializer)
    return Response(serializer.data, status.HTTP_201_CREATED)


class GetUserByIdViewset(viewsets.ViewSet):
  queryset = User.objects.all()
  serializer_class = getUserSerializer
  permission_classes = [IsUser | IsAdminUser]

  def create(self, request):
    user = User.objects.get(
        id=self.request.data['user_id'])
    if(user):
      return Response({"user": user.full_name}, status=status.HTTP_200_OK)
    else:
      return Response("User not found.", status=status.HTTP_404_NOT_FOUND)


class GetUserByMobileNumberViewset(viewsets.ViewSet):
  queryset = User.objects.all()
  serializer_class = getUserByMobileNumberSerializer
  permission_classes = [AllowAny]

  def create(self, request):
    if('mobile_number' in self.request.data):
      user = User.objects.filter(
          mobile_number=self.request.data['mobile_number'])
      if(user):
        return Response({
          "status" : True,
          "isUser": True,
          "detail" : "User exist."
        }, status=status.HTTP_200_OK)
      else:
        return Response({
          "status" : True,
          "isUser": False,
          "detail" : "User not found"
        }, status=status.HTTP_200_OK)
    else:
      return Response({
        'status' : False,
        'detail' : 'Mobile number is not provided.'
      }, status=status.HTTP_400_BAD_REQUEST)


class ForgotPasswordViewset(viewsets.ViewSet):
  queryset = User.objects.all()
  serializer_class = forgotPasswordSerializer
  permission_classes = [AllowAny]

  def create(self, request):
    user = User.objects.filter(
        mobile_number=self.request.data['mobile_number']).first()
    if user and not user.is_superuser:
      otp_obj = OTP.objects.filter(user=user.mobile_number, otp_type=OTP.Type.FORGOT_PASSWORD).first()
      if otp_obj:
        if otp_obj.matched:
          if 'password' in otp_obj.data:
            user.password = make_password(self.request.data['password'])
            user.save()
            otp_obj.delete()
            return Response("Password Changed", status=status.HTTP_200_OK)
        else:
          return Response({
              'status': False,
              'matched_failed': True,
              'detail': 'OTP does not matched'
          }, status=status.HTTP_200_OK)
      else:
        create_otp(user.mobile_number, self.request.data,
                   settings.PASSWORD_TEMPLATE, OTP.Type.FORGOT_PASSWORD, user=user)
        return Response({
            'otp': True,
            'status': True,
            'detail': 'OTP created.'
        }, status=status.HTTP_200_OK)

    else:
      return Response("User not found.", status=status.HTTP_404_NOT_FOUND)


class SendOTPViewset(APIView):
  permission_classes = [AllowAny]

  def post(self, request, *args, **kwargs):
    user = request.user
    mobile_number = request.data.get('mobile_number') if 'mobile_number' in request.data else user.mobile_number

    if not user.is_authenticated:
      user = User.objects.filter(mobile_number=mobile_number).first()

    if mobile_number:
      if user:
        create_otp(mobile_number, request.data, get_message_template(request.data.get('otp_type')),
                   request.data.get('otp_type'), user=user)
      else:
        create_otp(mobile_number, request.data,
                   get_message_template(request.data.get('otp_type')), request.data.get('otp_type'))
      return Response({
        'status' : True,
        'detail' : 'OTP sent successfully'
      }, status=status.HTTP_201_CREATED)
    else:
      return Response({
        'status' : False,
        'detail' : 'Mobile number not given.'
      }, status=status.HTTP_400_BAD_REQUEST)


class VerifyOTPViewset(APIView):
  permission_classes = [AllowAny]

  def post(self, request, *args, **kwargs):
    user = request.user
    # mobile_number = user.mobile_number if user.is_authenticated else request.data.get('mobile_number')
    mobile_number = request.data.get('mobile_number') if 'mobile_number' in request.data else user.mobile_number

    if mobile_number:
      otp_verify = verify_otp(mobile_number, request.data.get('otp'), request.data.get('otp_type'))
      if otp_verify:
        return Response({
          'status' : True,
          'detail' : 'OTP verify successful'
        }, status=status.HTTP_200_OK)
      else:
        return Response({
          'status': False,
          'detail': 'Invalid OTP'
        }, status=status.HTTP_200_OK)
    else:
      return Response({
        'status' : False,
        'detail' : 'Mobile number not given.'
      }, status=status.HTTP_400_BAD_REQUEST)

