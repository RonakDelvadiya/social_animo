
from rest_framework import serializers

from social_animo.serializers import DynamicFieldsModelSerializer, DynamicModelSerializer
from .models import *


class AddLikesSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = cntnt_likes
        fields = ('__all__')


class AddCommentsSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = cntnt_comments
        fields = ('__all__') 