from django.urls import path
from .views import current_user, UserList, UserPersonnelView, PersonnelViewSet

personnel_list_create = PersonnelViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

personnel_detail = PersonnelViewSet.as_view({
    'get': 'retrieve',
    'post': 'update',
    'delete': 'destroy'
})

urlpatterns = [
    path('current_user/', current_user),
    path('users/', UserList.as_view()),
    path('personnels/', personnel_list_create),
    path('personnels/<int:pk>/', personnel_detail),
]
