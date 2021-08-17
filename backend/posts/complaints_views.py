import json
from json import JSONEncoder
import re
import os

from django.shortcuts import render
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
from rest_framework.parsers import FormParser, MultiPartParser

from users.models import User
from posts.models import ComplaintsAndGrievances
from posts.complaints_serializers import ComplaintsAndGrievancesSerializer, ApproveComplaintsAndGrievancesSerializer, SolutionStatusComplaintsAndGrievancesSerializer, DeleteComplaintsAndGrievancesSerializer, UpdateComplaintsAndGrievancesSerializer
from service_auth.permissions import IsAdminUser, IsUser, IsUserReadOnly


class AllComplaintsAndGrievancesViewset(viewsets.ModelViewSet):
  queryset = ComplaintsAndGrievances.objects.all()
  serializer_class = ComplaintsAndGrievancesSerializer
  permission_classes = [IsAdminUser]

  def get_queryset(self):
    return ComplaintsAndGrievances.objects.order_by('-added')


class UserComplaintsAndGrievancesViewset(viewsets.ModelViewSet):
  queryset = ComplaintsAndGrievances.objects.all()
  serializer_class = ComplaintsAndGrievancesSerializer
  permission_classes = [IsUser]

  def get_queryset(self):
    return ComplaintsAndGrievances.objects.filter(user=self.request.user).order_by('-added')


class ComplaintsAndGrievancesViewset(viewsets.ModelViewSet):
  queryset = ComplaintsAndGrievances.objects.all()
  serializer_class = ComplaintsAndGrievancesSerializer
  permission_classes = [IsUser | IsAdminUser]

  def get_permissions(self):
    if self.request.method == 'POST':
      self.permission_classes = [IsUser]
    elif self.request.method == 'PUT':
      self.permission_classes = [IsUser]
    elif self.request.method == 'PATCH':
      self.permission_classes = [IsUser]

    return super(ComplaintsAndGrievancesViewset, self).get_permissions()

  def get_queryset(self):
    return ComplaintsAndGrievances.objects.filter(status=ComplaintsAndGrievances.ComplaintsAndGrievancesStatus.APPROVED).order_by('-added')

  def perform_create(self, serializer):
    serializer.save(user=self.request.user,
                    title=self.request.data.get('title'), description=self.request.data.get('description'))


class ApproveComplaintsAndGrievancesViewset(viewsets.ViewSet):
  queryset = ComplaintsAndGrievances.objects.all()
  serializer_class = ApproveComplaintsAndGrievancesSerializer
  permission_classes = [IsAdminUser]

  def create(self, request):
    complaint = ComplaintsAndGrievances.objects.get(id=self.request.data['complaints_id'])
    if(self.request.data['status'] == ComplaintsAndGrievances.ComplaintsAndGrievancesStatus.APPROVED):
      complaint.status = ComplaintsAndGrievances.ComplaintsAndGrievancesStatus.APPROVED
      complaint.save()
      return Response("Complaint approved.", status=status.HTTP_200_OK)
    elif(self.request.data['status'] == ComplaintsAndGrievances.ComplaintsAndGrievancesStatus.REJECTED):
      complaint.status = ComplaintsAndGrievances.ComplaintsAndGrievancesStatus.REJECTED
      complaint.save()
      return Response("Complaint rejected.", status=status.HTTP_200_OK)


class SolutionStatusComplaintsAndGrievancesViewset(viewsets.ViewSet):
  queryset = ComplaintsAndGrievances.objects.all()
  serializer_class = SolutionStatusComplaintsAndGrievancesSerializer
  permission_classes = [IsAdminUser]

  def create(self, request):
    complaint = ComplaintsAndGrievances.objects.get(id=self.request.data['complaints_id'])
    if(self.request.data['solution_status'] == ComplaintsAndGrievances.ComplaintsAndGrievancesSolutionStatus.SOLVED):
      complaint.solution_status = ComplaintsAndGrievances.ComplaintsAndGrievancesSolutionStatus.SOLVED
      complaint.save()
      return Response("Complaint solved.", status=status.HTTP_200_OK)
    elif(self.request.data['solution_status'] == ComplaintsAndGrievances.ComplaintsAndGrievancesSolutionStatus.UNSOLVED):
      complaint.solution_status = ComplaintsAndGrievances.ComplaintsAndGrievancesSolutionStatus.UNSOLVED
      complaint.save()
      return Response("Complaint unsolved.", status=status.HTTP_200_OK)


class DeleteComplaintsAndGrievancesViewset(viewsets.ViewSet):
  queryset = ComplaintsAndGrievances.objects.all()
  serializer_class = DeleteComplaintsAndGrievancesSerializer
  permission_classes = [IsUser | IsAdminUser]

  def create(self, request):
    complaint = ComplaintsAndGrievances.objects.get(id=self.request.data['complaints_id'])
    if(complaint):
      complaint.delete()
      return Response("Complaint deleted.", status=status.HTTP_200_OK)
    else:
      return Response("Complaint not found.", status=status.HTTP_404_NOT_FOUND)


class UpdateComplaintsAndGrievancesViewset(viewsets.ViewSet):
  queryset = ComplaintsAndGrievances.objects.all()
  serializer_class = UpdateComplaintsAndGrievancesSerializer
  permission_classes = [IsUser]

  def create(self, request):
    complaint = ComplaintsAndGrievances.objects.get(
        id=int(self.request.data.get('complaints_id')))
    if complaint:
      if(self.request.data.get('title') and self.request.data.get('description')):
        complaint.title = self.request.data.get('title')
        complaint.description = self.request.data.get('description')
        complaint.status = ComplaintsAndGrievances.ComplaintsAndGrievancesStatus.NEW
        complaint.solution_status = ComplaintsAndGrievances.ComplaintsAndGrievancesSolutionStatus.UNSOLVED
        complaint.save()
        return Response("Post updated.", status=status.HTTP_200_OK)
      else:
        return Response("Bad rquest.", status=status.HTTP_400_BAD_REQUEST)
    else:
      return Response("Post not found", status=status.HTTP_404_NOT_FOUND)
