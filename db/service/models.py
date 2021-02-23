from django.db import models

from db.account.models import Address, Translation, User
from db.core.models import BaseModel
from db.payment.models import Account, Payment


class ExpenseFile(models.Model):
    sku = models.CharField(max_length=128)
    url = models.FileField(upload_to="expense-files")
    img = models.ImageField(upload_to="expense-image")
    recource = models.CharField(max_length=128)

    def __str__(self):
        return self.sku


class ExpenseSupplier(BaseModel):
    address = models.ForeignKey(Address, related_name="supplier", on_delete=models.SET_NULL, null=True)
    account = models.ForeignKey(Account, related_name="supplier", on_delete=models.SET_NULL, null=True)
    company_name = models.CharField(max_length=128)
    supplier = models.OneToOneField(User, related_name="supplier", on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.supplier.name 


class ExpenseCategory(BaseModel):
    translations = models.ManyToManyField(
        Translation, 
        related_name="expense_categories"
    )
    name = models.CharField(max_length=128)
    description = models.TextField()

    def __str__(self):
        return self.name


class Expense(BaseModel):
    translations = models.ManyToManyField(
        Translation, 
        related_name="expenses"
    )
    file = models.ForeignKey(ExpenseFile, on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(Payment, related_name="expense", on_delete=models.SET_NULL, null=True)
    invoice = models.ForeignKey("orders.Invoice", related_name="expense", on_delete=models.SET_NULL, null=True)
    supplier = models.ForeignKey(ExpenseSupplier, related_name="expense", on_delete=models.CASCADE)
    expense_tag_category = models.ForeignKey(ExpenseCategory, related_name="expense", on_delete=models.SET_NULL, null=True)
    date = models.DateField(auto_now=True)
    uid = models.CharField(max_length=64)
    total_price = models.DecimalField(max_digits=7, decimal_places=2)
    #expense items
    bookkeeping_status = models.CharField(max_length=64)
    is_locked = models.BooleanField(default=True)

    def __str__(self):
        return self.uid


class ExpenseItem(BaseModel):
    translations = models.ManyToManyField(
        Translation, 
        related_name="expense_items"
    )
    name = models.CharField(max_length=128)
    description = models.TextField()
    expense = models.ForeignKey(Expense, related_name="expense_items", on_delete=models.CASCADE)

    def __str__(self):
        return self.name