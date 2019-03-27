from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
  camera = serializers.StringRelatedField()

  class Meta:
    model = Notification
    fields = ('_type', 'timestamp', 'camera')