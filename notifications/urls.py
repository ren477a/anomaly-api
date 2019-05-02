from django.urls import path
from .views import NotificationList, NotificationListCreate

urlpatterns = [
    path('', NotificationListCreate.as_view())
]