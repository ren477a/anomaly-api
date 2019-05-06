import json
import traceback

from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from rest_framework import permissions, status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from django.shortcuts import get_object_or_404

from notifications.models import Person

from .serializers import (CreatePersonnelSerializer, PersonSerializer,
                          UserSerializer, UserSerializerWithToken)


@api_view(['GET'])
def current_user(request):
    """
    Determine the current user by their token, and return their data
    """

    serializer = UserSerializer(request.user)
    return Response(serializer.data)


class UserList(APIView):
  """
  Create a new user. It's called 'UserList' because normally we'd have a get
  method here too, for retrieving a list of all User objects.
  """

  permission_classes = (permissions.AllowAny,)

  def get(self, request, format=None):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

  def post(self, request, format=None):
    serializer = UserSerializerWithToken(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserPersonnelView(APIView):
  permission_classes = (permissions.IsAuthenticated,)

  def get(self, request, format=None):
    try:
      print(request.user.person)
      persons = Person.objects.filter(admin=request.user.person)
      serializer = PersonSerializer(persons, many=True)
      return Response(serializer.data, status=status.HTTP_200_OK)
    except:
      print(traceback.format_exc())
      return Response([], status=status.HTTP_404_NOT_FOUND)

  def post(self, request, format=None):
    try:
      request_data = JSONParser().parse(request)
      person_serializer = CreatePersonnelSerializer(data=request_data)
      user_serializer = UserSerializerWithToken(data=request_data)
      if person_serializer.is_valid() and user_serializer.is_valid():
          user_serializer.save()
          user_data = user_serializer.validated_data
          personnel_user = User.objects.get(username=user_data.get('username'))
          person_data = person_serializer.validated_data
          person_data.pop('username')
          person_data.pop('password')
          personnel = Person.objects.create(
              **person_data, user=personnel_user, admin=request.user.person)
          return Response({
              'user_id': personnel.user.pk,
              'person_id': personnel.pk
          }, status=status.HTTP_201_CREATED)
    except:
      print(traceback.format_exc())
    return Response(person_serializer.errors or user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PersonnelViewSet(viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticated,)

    def list(self, request):
        queryset = Person.objects.filter(admin=request.user.person)
        serializer = PersonSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Person.objects.filter(admin=request.user.person)
        personnel = get_object_or_404(queryset, pk=pk)
        serializer = PersonSerializer(personnel)
        return Response(serializer.data)

    def create(self, request):
      try:
        request_data = JSONParser().parse(request)
        person_serializer = CreatePersonnelSerializer(data=request_data)
        user_serializer = UserSerializerWithToken(data=request_data)
        if person_serializer.is_valid() and user_serializer.is_valid():
            user_serializer.save()
            user_data = user_serializer.validated_data
            personnel_user = User.objects.get(
                username=user_data.get('username'))
            person_data = person_serializer.validated_data
            person_data.pop('username')
            person_data.pop('password')
            personnel = Person.objects.create(
                **person_data, user=personnel_user, admin=request.user.person)
            return Response({
                'user_id': personnel.user.pk,
                'person_id': personnel.pk
            }, status=status.HTTP_201_CREATED)
      except:
        print(traceback.format_exc())
      return Response(person_serializer.errors or user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
      queryset = Person.objects.filter(admin=request.user.person)
      personnel = get_object_or_404(queryset, pk=pk)
      serializer = PersonSerializer(personnel, data=request.data, partial=True)
      if serializer.is_valid(raise_exception=True):
        serializer.save()
      return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
      queryset = Person.objects.filter(admin=request.user.person)
      personnel = get_object_or_404(queryset, pk=pk)
      personnel.delete()
      return Response({'success': True}, status=status.HTTP_200_OK)
