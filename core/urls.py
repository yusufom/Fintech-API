from django.urls import path, include
from . import views
from .views import IndexView

app_name = "core-api"

urlpatterns = [
    
    path('', IndexView.as_view(), name='Index'),
]