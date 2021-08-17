from rest_framework import serializers
from users.models import User, FamilyDetails
from posts.serializers import PostSerializer

class UserSerializer(serializers.ModelSerializer):
  password = serializers.CharField(write_only=True)
  class Meta:
    model = User
    fields = (
      'id',
      'mobile_number',
      'password',
      'full_name',
      'address',
      'company',
      'designation',
      'family_members',
      'role',
      'email',
      'is_active',
      'date_joined'
    )
    extra_kwargs = {
      'password': { 'write_only': True },
    }

class GetUserSerializer(serializers.ModelSerializer):
  post_user_id = PostSerializer(many=True, read_only=True)
  class Meta:
    model = User
    depth = 1
    fields = (
      'id',
      'mobile_number',
      'full_name',
      'address',
      'company',
      'designation',
      'family_members',
      'role',
      'email',
      'is_active',
      'date_joined',
      'post_user_id',
    )
    extra_kwargs = {
      'post_user_id': {'read_only': True},
    }
    read_only_fields = ('post_user_id',)


class FamilySerializer(serializers.ModelSerializer):
  class Meta:
    model = FamilyDetails
    fields = (
      'id',
      'user',
      'relation',
      'member_name'
    )


class userStatusSerializer(serializers.Serializer):
  status = serializers.CharField(max_length=20)
  user_id = serializers.CharField(max_length=20)


class getUserSerializer(serializers.Serializer):
  user_id = serializers.CharField(max_length=20)


class getUserByMobileNumberSerializer(serializers.Serializer):
  mobile_number = serializers.CharField(max_length=20)


class forgotPasswordSerializer(serializers.Serializer):
  mobile_number = serializers.CharField(max_length=20)
  password = serializers.CharField(max_length=20)


class UpdatePasswordSerializer(serializers.Serializer):
  password = serializers.CharField(max_length=20)
  new_password = serializers.CharField(max_length=20)
