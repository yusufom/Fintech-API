from .serializers import AccountSerializers, TransactionSerializers
from django.http import HttpRequest, HttpResponse
from rest_framework.response import Response
from rest_framework import permissions, status, viewsets
from rest_framework.views import APIView
from core.models import Account, Transaction
from rest_api_payload import error_response, success_response
from authentication.models import User
from rest_framework import generics, status, views, viewsets
from rest_framework.decorators import action


class AccountView(APIView):

  # permissions_classes = [permissions.IsAuthenticated]
  
  def get(self, request, id, *args, **kwargs):
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

class DepositView(generics.GenericAPIView):
  serializer_class = TransactionSerializers
  
  # permissions_classes = [permissions.IsAuthenticated]
  
  def post(self, request, id, *args, **kwargs):
    """
    It takes in a request, checks if the user and account exists, validates the data, checks if the
    amount is greater than 0, saves the data and returns a response
    
    :param request: The request object \n
    :param id: The id of the user whose account is to be credited \n
    :param amount: The amount to be deposited \n
    :return: A response object with the status code and the data
    """
    
    try:
      user = User.objects.get(id=id)
    except User.DoesNotExist:
      return Response(status=status.HTTP_404_NOT_FOUND)

    try:
      account = Account.objects.get(user=user)
    except Account.DoesNotExist:
      return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = TransactionSerializers(data=request.data)

    if serializer.is_valid():
      deposit_amount = serializer.validated_data.get("amount")
      if deposit_amount >= 0:
        serializer.save(
          user = user,
          account = account,
          amount = deposit_amount,
          transaction_type = "Deposit"
        )
        payload = success_response(
          status = "Success",
          message = f'{deposit_amount} successfully deposited',
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


class WithdrawalView(generics.GenericAPIView):
  serializer_class = TransactionSerializers

  
  # permissions_classes = [permissions.IsAuthenticated]
  
  def post(self, request, id, *args, **kwargs):
    """
    It checks if the user exists, if the account exists, if the amount is less than the balance, if
    the amount is greater than 0, and if all these conditions are met, it saves the transaction
    
    :param request: The request object \n
    :param id: This is the id of the user whose account is to be credited \n
    :param amount: This is the amount to be withdrawn \n
    :return: The transactor amount
    """
    try:
      user = User.objects.get(id=id)
    except User.DoesNotExist:
      return Response(status=status.HTTP_404_NOT_FOUND)

    try:
      account = Account.objects.get(user=user)
    except Account.DoesNotExist:
      return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = TransactionSerializers(data=request.data)
    serializer = TransactionSerializers(data=request.data)
    if serializer.is_valid():
      amount_withdrawn = serializer.validated_data.get("amount")
      if int(amount_withdrawn) > int(account.balance):
        payload =error_response(
          status = "Failed",
          message = "Amount can not be more than balance"
        )
        return Response(data=payload, status=status.HTTP_403_FORBIDDEN)
      elif int(amount_withdrawn) < 0:
        payload =error_response(
          status = "Failed",
          message = "Amount can not be less than 0"
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

