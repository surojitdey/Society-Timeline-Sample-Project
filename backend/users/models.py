from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator

from .managers import CustomUserManager


def my_default_json():
    return {'foo': 'bar'}


class User(AbstractUser):
  class Role(models.TextChoices):
    ADMIN = 'admin', _('admin')
    USER = 'user', _('user')

  username = None
  first_name = None
  last_name = None
  ROLE = None
  mobile_number = models.CharField(_('mobile number'), max_length=20, unique=True)
  full_name = models.CharField(_('full name'), max_length=100, blank=False)
  address = models.TextField(_('address'), max_length=500, blank=False)
  company = models.CharField(_('company'), max_length=50, blank=True)
  designation = models.CharField(_('designation'), max_length=50, blank=True)
  family_members = models.IntegerField(_('numbers of family members'), validators=[MinValueValidator(0), MaxValueValidator(10)], blank=True, default=0)
  role = models.CharField(_('user role'), max_length=15, choices=Role.choices, default=Role.USER, blank=True)

  USERNAME_FIELD = 'mobile_number'
  REQUIRED_FIELDS = []

  objects = CustomUserManager()

  def __str__(self):
    return self.mobile_number


class FamilyDetails(models.Model):
  class Relations(models.TextChoices):
    HUSBAND = 'husband', _('husband')
    WIFE = 'wife', _('wife')
    FATHER = 'father', _('father')
    MOTHER = 'mother', _('mother')
    SON = 'son', _('son')
    DAUGHTER = 'daughter', _('daughter')
    BROTHER = 'brother', _('brother')
    SISTER = 'sister', _('sister')
    OTHER = 'other', _('other')

  user = models.ForeignKey(User, on_delete=models.CASCADE)
  relation = models.CharField(_('type of relation'), choices=Relations.choices, default=Relations.OTHER, max_length=50, blank=False)
  member_name = models.CharField(_('family member name'), max_length=50, blank=False)

  def __str__(self):
    return self.relation


class OTP(models.Model):
  class Type(models.TextChoices):
    PASSWORD = 'password', _('password')
    FORGOT_PASSWORD = 'forgot_password', _('forgot_password')
    NUMBER_CHANGE = 'number_change', _('number_change')
    SIGNUP = 'signup', _('signup')

  otp = models.CharField(_('otp'), max_length=4, blank=False)
  user = models.CharField(_('user'), max_length=20, blank=False)
  created = models.DateTimeField(auto_now_add=True)
  active = models.BooleanField(_('active'), default=True, blank=True)
  matched = models.BooleanField(_('matched'), default=False, blank=True)
  data = models.JSONField(default=my_default_json)
  otp_type = models.CharField(_('otp type'), choices=Type.choices,
                              max_length=50, blank=True)
