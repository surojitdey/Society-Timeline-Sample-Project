from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from posts.models import *


class PostSerializer(serializers.ModelSerializer):
  user = serializers.SlugRelatedField(
      read_only=True,
      slug_field='id'
  )
  full_name = serializers.CharField(source='user.full_name', read_only=True)

  class Meta:
    model = Post
    fields = (
        'id',
        'user',
        'media_file',
        'thumbnail',
        'added',
        'title',
        'description',
        'post_status',
        'full_name'
    )


class ApprovePostSerializer(serializers.Serializer):
  post_status = serializers.CharField(max_length=20)
  post_id = serializers.CharField(max_length=20)


class UpdatePostSerializer(serializers.Serializer):
  post_id = serializers.CharField(max_length=20)
  title = serializers.CharField(max_length=100)
  description = serializers.CharField(max_length=2000)
  media_file = serializers.FileField()


class DeletePostSerializer(serializers.Serializer):
  post_id = serializers.CharField(max_length=20)


class PostCommentSerializer(serializers.ModelSerializer):
  user = serializers.SlugRelatedField(
      read_only=True,
      slug_field='id'
  )
  full_name = serializers.CharField(source='user.full_name', read_only=True)

  class Meta:
    model = PostComment
    fields = (
        'id',
        'user',
        'post',
        'comment',
        'added',
        'full_name'
    )


class DeletePostCommentSerializer(serializers.Serializer):
  comment_id = serializers.CharField(max_length=20)
