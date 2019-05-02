from rest_framework import serializers
from .models import Notification, Person


class NotificationListSerializer(serializers.ModelSerializer):
  camera = serializers.StringRelatedField()

  class Meta:
    model = Notification
    fields = '__all__'


class NotificationCreateSerializer(serializers.ModelSerializer):

  class Meta:
    model = Notification
    fields = '__all__'


class PersonSerializer(serializers.ModelSerializer):
  class Meta:
    model = Person
    fields = '__all__'