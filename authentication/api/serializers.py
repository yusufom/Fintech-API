from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from authentication.models import *



class CreateUserSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email','username', 'password', 'first_name', 'last_name', 'phone' )