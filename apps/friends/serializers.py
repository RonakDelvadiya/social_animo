
from rest_framework import serializers

from social_animo.serializers import DynamicFieldsModelSerializer, DynamicModelSerializer
from profiles.models import prfl_profile
from django.contrib.auth.models import User


class UserSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = User
        fields = ('first_name','last_name', 'username')


class SearchFriendsProfileSerializer(DynamicFieldsModelSerializer):
    user = UserSerializer()
    class Meta:
        model = prfl_profile
        fields = ('profile_name','user')