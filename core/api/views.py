from .serializers import AccountSerializers, TransactionSerializers
from django.http import HttpRequest, HttpResponse
from rest_framework.response import Response
from rest_framework import permissions, status, viewsets
from rest_framework.views import APIView
from core.models import Account, Transaction
from rest_api_payload import error_response, success_response
from authentication.models import User
import djoser
from rest_framework import generics, status, views, viewsets
from rest_framework.decorators import action


class AccountView(APIView):
  
  """
    Returns a list of all **active** accounts in the system.

    For more details on how accounts are activated please [see here][ref].

    [ref]: http://example.com/activating-accounts
    """
  
  # permissions_classes = [permissions.IsAuthenticated]
  
  def get(self, request, id):
    try: 
      queryset = Account.objects.get(id=id)
      serializer = AccountSerializers(queryset)
      payload = success_response(
          status="success",
          message="Account Balance retrieved!",
          data=serializer.data
      )
      return Response(data=payload, status=status.HTTP_200_OK)
    except Account.DoesNotExist:
      payload = error_response(
          status="failed",
          message="Empty"
      )
      return Response(data=payload, status=status.HTTP_204_NO_CONTENT)

class DepositView(APIView):
  
  # permissions_classes = [permissions.IsAuthenticated]
  
  def post(self, request, id):
    user = User.objects.get(id=id)
    account = Account.objects.get(user=user)
    serializer = TransactionSerializers(data=request.data)
    if serializer.is_valid():
      amount_withdrawn = serializer.validated_data.get("amount")
      if amount_withdrawn >= 0:
        serializer.save(
          user = user,
          account = account,
          amount = serializer.validated_data.get("amount"),
          transaction_type = "Deposit"
        )
        payload = success_response(
          status = "Success",
          message = f'{serializer.validated_data.get("amount")} successfully deposited',
          data = serializer.data
          )
        return Response(data=payload, status=status.HTTP_201_CREATED)
      else:
        payload = error_response (
          status  = 'failed',
          message = "Amount cannot be less than 0"
        )
        return Response(data=payload, status=status.HTTP_406_NOT_ACCEPTABLE)
    return Response(status=status.HTTP_400_BAD_REQUEST)


class WithdrawalView(APIView):
  
  # permissions_classes = [permissions.IsAuthenticated]
  
  def post(self, request, id, *args, **kwargs):
    """
    It checks if the amount to be withdrawn is less than the account balance, if it is, it saves the
    transaction, else it returns an error message
    
    :param request: The request object \n
    :param id: This is the id of the user whose account is to be credited \n
    :param amount: This is the amount to be withdrawn \n
    :return: The response is a json object with the status, message and data.
    """
    user = User.objects.get(id=id)
    account = Account.objects.get(user=user)
    serializer = TransactionSerializers(data=request.data)
    if serializer.is_valid():
      amount_withdrawn = serializer.validated_data.get("amount")
      if int(amount_withdrawn) > int(account.balance):
        payload =error_response(
          status = "Failed",
          message = "Amount can not be more than balance"
        )
        return Response(data=payload, status=status.HTTP_403_FORBIDDEN)
      else:
        serializer.save(
          user = user,
          account = account,
          amount = amount_withdrawn,
          transaction_type = "Withdrawal"
        )
        payload = success_response(
          status = "Success",
          message = f'{amount_withdrawn} successfully withdrawn',
          data = serializer.data
          )
        return Response(data=payload, status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_400_BAD_REQUEST)

