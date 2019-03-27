from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from rest_framework import permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import NotificationSerializer
from .models import Notification

"""
User Authentication

Camera
GET
Edit camera name

Notification
Websocket live notification
GET (for history)
Delete (Clear history)
"""

class NotificationList(APIView):
  permission_classes = (permissions.AllowAny,)

  def get(self, request, format=None):
    items = request.GET.get('items', None)
    notifications = Notification.objects.all()

    if items:
      notifications = Notification.objects.order_by('timestamp')[:int(items)]

    
    serializer = NotificationSerializer(notifications, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


