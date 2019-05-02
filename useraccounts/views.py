from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from rest_framework import permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from notifications.models import Person
from notifications.serializers import PersonSerializer
from .serializers import UserSerializer, UserSerializerWithToken
import traceback


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
  

class UserUnderlingView(APIView):
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
    serializer = PersonSerializer(request)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)