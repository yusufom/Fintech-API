from django.urls import path, include
from . import views
from .views import AccountView, DepositView, WithdrawalView

app_name = "core"

urlpatterns = [
    
    path('account/<int:id>/', AccountView.as_view(), name='account_balance'),
    path('deposit/<int:id>/', DepositView.as_view(), name='deposit'),
    path('withdraw/<int:id>/', WithdrawalView.as_view(), name='withdraw'),
]