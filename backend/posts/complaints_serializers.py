from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from posts.models import *


class ComplaintsAndGrievancesSerializer(serializers.ModelSerializer):
  user = serializers.SlugRelatedField(
      read_only=True,
      slug_field='id'
  )
  full_name = serializers.CharField(source='user.full_name', read_only=True)

  class Meta:
    model = ComplaintsAndGrievances
    fields = (
        'id',
        'user',
        'added',
        'title',
        'description',
        'status',
        'solution_status',
        'full_name'
    )


class ApproveComplaintsAndGrievancesSerializer(serializers.Serializer):
  status = serializers.CharField(max_length=20)
  complaints_id = serializers.CharField(max_length=20)


class SolutionStatusComplaintsAndGrievancesSerializer(serializers.Serializer):
  solution_status = serializers.CharField(max_length=20)
  complaints_id = serializers.CharField(max_length=20)


class DeleteComplaintsAndGrievancesSerializer(serializers.Serializer):
  complaints_id = serializers.CharField(max_length=20)


class UpdateComplaintsAndGrievancesSerializer(serializers.Serializer):
  complaints_id = serializers.CharField(max_length=20)
  title = serializers.CharField(max_length=100)
  description = serializers.CharField(max_length=2000)
