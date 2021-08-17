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
from events.models import Events, News
from events.serializers import *
from service_auth.permissions import IsAdminUser, IsUser, IsUserReadOnly


class EventsViewset(viewsets.ModelViewSet):
  queryset = Events.objects.all()
  serializer_class = EventSerializer
  permission_classes = [AllowAny]
  parser_classes = (MultiPartParser, FormParser,)

  def get_permissions(self):
    if self.request.method == 'POST':
      self.permission_classes = [IsAdminUser]
    elif self.request.method == 'PUT':
      self.permission_classes = [IsAdminUser]
    elif self.request.method == 'PATCH':
      self.permission_classes = [IsAdminUser]
    return super(EventsViewset, self).get_permissions()

  def get_queryset(self):
    return Events.objects.order_by('-added')

  def perform_create(self, serializer):
    serializer.save()


class UpdateEventViewset(viewsets.ViewSet):
  queryset = Events.objects.all()
  serializer_class = EventSerializer
  permission_classes = [IsAdminUser]
  parser_classes = (MultiPartParser, FormParser,)

  def create(self, request):
    event = Events.objects.get(id=int(self.request.data.get('id')))
    if event:
      if(self.request.data.get('media_file')):
        event.title = self.request.data.get('title')
        event.description = self.request.data.get('description')
        event.media_file = self.request.data.get('media_file')
        event.event_date = self.request.data.get('event_date')
        event.event_time = self.request.data.get('event_time')
        event.time_convention = self.request.data.get('time_convention')
        event.save()
        return Response("Events updated.", status=status.HTTP_200_OK)
      else:
        event.title = self.request.data.get('title')
        event.description = self.request.data.get('description')
        event.event_date = self.request.data.get('event_date')
        event.event_time = self.request.data.get('event_time')
        event.time_convention = self.request.data.get('time_convention')
        event.save()
        return Response("Events updated.", status=status.HTTP_200_OK)
    else:
      return Response("Events not found", status=status.HTTP_404_NOT_FOUND)


class DeleteEventViewset(viewsets.ViewSet):
  queryset = Events.objects.all()
  serializer_class = DeleteSerializer
  permission_classes = [IsAdminUser]

  def create(self, request):
    event = Events.objects.get(id=int(self.request.data.get('event_id')))
    if event:
      event.delete()
      return Response("Events deleted.", status=status.HTTP_200_OK)
    else:
      return Response("Events not found", status=status.HTTP_404_NOT_FOUND)


class LimitEventsViewset(viewsets.ReadOnlyModelViewSet):
  queryset = Events.objects.all()
  serializer_class = EventSerializer
  permission_classes = [AllowAny]

  def get_queryset(self):
    return Events.objects.order_by('-added')[:3]


class NewsViewset(viewsets.ModelViewSet):
  queryset = News.objects.all()
  serializer_class = NewsSerializer
  permission_classes = [AllowAny]
  parser_classes = (MultiPartParser, FormParser,)

  def get_permissions(self):
    if self.request.method == 'POST':
      self.permission_classes = [IsAdminUser]
    elif self.request.method == 'PUT':
      self.permission_classes = [IsAdminUser]
    elif self.request.method == 'PATCH':
      self.permission_classes = [IsAdminUser]
    return super(NewsViewset, self).get_permissions()

  def get_queryset(self):
    return News.objects.order_by('-added')

  def perform_create(self, serializer):
    serializer.save()


class UpdateNewsViewset(viewsets.ViewSet):
  queryset = News.objects.all()
  serializer_class = NewsSerializer
  permission_classes = [IsAdminUser]
  parser_classes = (MultiPartParser, FormParser,)

  def create(self, request):
    news = News.objects.get(id=int(self.request.data.get('id')))
    if news:
      if(self.request.data.get('media_file')):
        news.title = self.request.data.get('title')
        news.description = self.request.data.get('description')
        news.media_file = self.request.data.get('media_file')
        news.save()
        return Response("News updated.", status=status.HTTP_200_OK)
      else:
        news.title = self.request.data.get('title')
        news.description = self.request.data.get('description')
        news.save()
        return Response("News updated.", status=status.HTTP_200_OK)
    else:
      return Response("News not found", status=status.HTTP_404_NOT_FOUND)


class DeleteNewsViewset(viewsets.ViewSet):
  queryset = News.objects.all()
  serializer_class = DeleteNewsSerializer
  permission_classes = [IsAdminUser]

  def create(self, request):
    news = News.objects.get(id=int(self.request.data.get('event_id')))
    if news:
      news.delete()
      return Response("News deleted.", status=status.HTTP_200_OK)
    else:
      return Response("News not found", status=status.HTTP_404_NOT_FOUND)


class LimitNewsViewset(viewsets.ReadOnlyModelViewSet):
  queryset = News.objects.all()
  serializer_class = NewsSerializer
  permission_classes = [AllowAny]

  def get_queryset(self):
    return News.objects.order_by('-added')[:4]
