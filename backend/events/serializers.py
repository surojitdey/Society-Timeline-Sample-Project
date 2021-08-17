from rest_framework import serializers
from events.models import *


class EventSerializer(serializers.ModelSerializer):
  class Meta:
    model = Events
    fields = (
        'id',
        'media_file',
        'thumbnail',
        'added',
        'title',
        'description',
        'event_date',
        'event_time',
        'time_convention'
    )

class DeleteSerializer(serializers.Serializer):
  event_id = serializers.CharField(max_length=20)


class NewsSerializer(serializers.ModelSerializer):
  class Meta:
    model = News
    fields = (
        'id',
        'media_file',
        'added',
        'title',
        'description',
        'thumbnail'
    )


class DeleteNewsSerializer(serializers.Serializer):
  news_id = serializers.CharField(max_length=20)
