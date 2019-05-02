from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from rest_framework import permissions, status
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import NotificationListSerializer, NotificationCreateSerializer
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
  permission_classes = (permissions.IsAuthenticated,)

  def get(self, request, format=None):
    items = request.GET.get('items', None)
    # TODO: Filter by logged in user usr ListAPIView
    notifications = Notification.objects.all()

    if items:
      notifications = Notification.objects.order_by('timestamp')[:int(items)]

    
    serializer = NotificationSerializer(notifications, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


class NotificationListCreate(generics.ListCreateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationCreateSerializer
    permission_classes = (permissions.AllowAny,)

    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = NotificationListSerializer(queryset, many=True)
        return Response(serializer.data)