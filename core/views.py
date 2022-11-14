from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework import generics

# Create your views here.

class IndexView(generics.ListAPIView):
  permissions_classes = [permissions.AllowAny]

  
  def get(self, request):
    payload = {
        "Documentation" : "/docs",
        "login" : "/auth/jwt/create/",
        "register": "/auth/users/",
        "withdraw": "/api/withdraw/{user_id}/",
        "deposit": "/api/deposit/{user_id}/",
        "balance": "/api/account/{user_id}/"
    }
    return Response(data=payload, status=status.HTTP_200_OK)