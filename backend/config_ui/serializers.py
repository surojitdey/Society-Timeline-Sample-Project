from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from config_ui.models import *


class ContactSerializer(serializers.ModelSerializer):
  class Meta:
    model = ContactDetails
    fields = (
        'id',
        'community_name',
        'appartment_name',
        'address_one',
        'address_two',
        'city',
        'pincode',
        'contact_number',
        'email',
        'show_address',
        'show_number',
        'show_email'
    )
