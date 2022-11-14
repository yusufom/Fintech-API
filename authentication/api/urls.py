from django.urls import path, include
from . import views
import djoser

app_name = "authentication"

urlpatterns = [
    
    path('', include('djoser.urls.jwt')),
    path('', include('djoser.urls')),
]