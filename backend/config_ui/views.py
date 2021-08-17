import json
from json import JSONEncoder

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.hashers import make_password, check_password

from rest_framework import viewsets, status, permissions
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.parsers import JSONParser
from rest_framework.request import Request
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.views import APIView


from config_ui.models import *
from config_ui.serializers import *
from service_auth.permissions import IsUser, IsUserReadOnly, IsAdminUser


class ContactsViewset(viewsets.ModelViewSet):
  queryset = ContactDetails.objects.all()
  serializer_class = ContactSerializer
  permission_classes = [IsAdminUser]

  def get_permissions(self):
    if self.request.method == 'POST':
      self.permission_classes = (IsAdminUser,)
    elif self.request.method == 'PUT':
      self.permission_classes = [IsAdminUser]
    elif self.request.method == 'PATCH':
      self.permission_classes = [IsAdminUser]
    elif self.request.method == 'GET':
      self.permission_classes = [AllowAny]

    return super(ContactsViewset, self).get_permissions()

  def create(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    self.perform_create(serializer)
    return Response(serializer.data, status.HTTP_201_CREATED)


class UpdateContactsViewset(viewsets.ViewSet):
  queryset = ContactDetails.objects.all()
  serializer_class = ContactSerializer
  permission_classes = [IsAdminUser]

  def get_permissions(self):
    if self.request.method == 'POST':
      self.permission_classes = (IsAdminUser,)
    elif self.request.method == 'PUT':
      self.permission_classes = [IsAdminUser]
    elif self.request.method == 'PATCH':
      self.permission_classes = [IsAdminUser]
    elif self.request.method == 'GET':
      self.permission_classes = [AllowAny]

    return super(UpdateContactsViewset, self).get_permissions()

  def create(self, request, *args, **kwargs):
    contacts = ContactDetails.objects.get(id=int(self.request.data.get('id')))
    if contacts:
      contacts.community_name = self.request.data.get('community_name')
      contacts.appartment_name = self.request.data.get('appartment_name')
      contacts.address_one = self.request.data.get('address_one')
      contacts.address_two = self.request.data.get('address_two')
      contacts.city = self.request.data.get('city')
      contacts.pincode = self.request.data.get('pincode')
      contacts.contact_number = self.request.data.get('contact_number')
      contacts.email = self.request.data.get('email')
      contacts.show_address = self.request.data.get('show_address')
      contacts.show_number = self.request.data.get('show_number')
      contacts.show_email = self.request.data.get('show_email')
      contacts.save()
      return Response('contacts updated', status.HTTP_201_CREATED)
    else:
      return Response("Contacts not found", status=status.HTTP_404_NOT_FOUND)
