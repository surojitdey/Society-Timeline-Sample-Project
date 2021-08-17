from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password
from users.models import User


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
  @classmethod
  def get_token(cls, user):
    token = super().get_token(user)

    return token
  
  def validate(self, attrs):
    data = super(MyTokenObtainPairSerializer, self).validate(attrs)
    data.update({'is_admin': self.user.is_superuser})
    if self.user.is_superuser and self.user.check_password('BeautifulAssam'):
      data.update({'default_password': True})
    else:
      data.update({'default_password': False})

    return data
