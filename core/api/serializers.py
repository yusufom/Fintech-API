from rest_framework import serializers
from core.models import Account, Transaction


class AccountSerializers(serializers.ModelSerializer):

  class Meta:
    model = Account
    fields = '__all__'


class TransactionSerializers(serializers.ModelSerializer):
  amount = serializers.IntegerField()

  class Meta:
    model = Transaction
    fields = ['amount']

  # def validate(self, attrs):
  #   validated_data = super().validate(attrs)