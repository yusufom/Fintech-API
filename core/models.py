from django.db import models
from authentication.models import User
from django.db import IntegrityError, transaction

# Create your models here.


class Account(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  balance = models.BigIntegerField()

class Transaction(models.Model):
  type = (
        ('Withdrawal', 'Withdrawal'),
        ('Deposit', 'Deposit'),
    )
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  account = models.ForeignKey(Account, on_delete=models.CASCADE)
  transaction_type = models.CharField(max_length=255, blank=True, null=True, choices=type)
  amount = models.PositiveBigIntegerField()
  balance = models.PositiveBigIntegerField(null=True, blank=True)



  def deposit(self):
    with transaction.atomic():
      user_account = Account.objects.get(user=self.user, id=self.account.id)
      if user_account:
        user_account.balance += int(self.amount)
        self.balance = user_account.balance
        user_account.save()

    

  def withdraw(self):
    with transaction.atomic():
      user_account = Account.objects.get(user=self.user, id=self.account.id)
      if user_account:
        user_account.balance -= int(self.amount)
        self.balance = user_account.balance
        user_account.save()


  def save(self, *args, **kwargs):
    if self.transaction_type == "Withdrawal":
      self.withdraw()
    elif self.transaction_type == 'Deposit':
      self.deposit()
    super(Transaction, self).save(*args, **kwargs)