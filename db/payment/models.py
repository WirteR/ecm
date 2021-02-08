from django.db import models

from db.core.models import BaseModel

# Create your models here.

class Account(BaseModel):
    translations = models.ManyToManyField(
        'account.Translation', 
        related_name="accounts",
        null=True
    )
    name = models.CharField(max_length=128)
    description = models.TextField()
    account_number = models.CharField(max_length=128)
    account_type = models.CharField(max_length=64)
    split_profit = models.DecimalField(max_digits=7, decimal_places=2)
    account_cost = models.DecimalField(max_digits=7, decimal_places=2)
    account_profit = models.DecimalField(max_digits=7, decimal_places=2)
    default_for = models.CharField(max_length=64)
    default_year = models.CharField(max_length=6)
    online_account = models.CharField(max_length=128)
    paypal_email = models.EmailField(max_length=128)
    opening_date = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.account_number} -> {self.name}"


class Payment(BaseModel):
    translations = models.ManyToManyField(
        'account.Translation', 
        related_name="payments",
        null=True
    )
    account = models.ForeignKey(Account, related_name="payment", on_delete=models.CASCADE)
    status = models.CharField(max_length=64)
    type = models.CharField(max_length=24)
    amount = models.DecimalField(max_digits=7, decimal_places=2)
    name = models.CharField(max_length=128)
    description = models.TextField()
    note = models.CharField(max_length=128)
    marketplace_id = models.CharField(max_length=128)
    bookkeeping_status = models.CharField(max_length=64)
    is_locked = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.type} | {self.name}"
    