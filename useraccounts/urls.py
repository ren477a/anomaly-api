from django.urls import path
from .views import current_user, UserList, UserPersonnelView

urlpatterns = [
    path('current_user/', current_user),
    path('users/', UserList.as_view()),
    path('personnels/', UserPersonnelView.as_view()),
]