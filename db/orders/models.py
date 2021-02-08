from django.db import models

from db.account.models import Address, Customer
from db.core.models import BaseModel, User
from db.payment.models import Account, Payment
from db.product.models import Product, ProductService, QualityData
from db.warehouse.models import WarehouseStorage

# Create your models here.


class Invoice(BaseModel):
    translations = models.ManyToManyField(
        'account.Translation', 
        related_name="invoices"
    )
    url = models.CharField(max_length=256)
    date = models.DateField(auto_now=True)
    num = models.IntegerField()


class PurchaseOrder(BaseModel):
    #serialized_products - serializer
    seller = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    translations = models.ManyToManyField(
        'account.Translation', 
        related_name="purchase_orders"
    )
    creditor = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    user_owner = models.ForeignKey(User, on_delete=models.CASCADE)
    invoice = models.ForeignKey(Invoice, on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)

    uid = models.CharField(max_length=64)
    order_date = models.DateField(auto_now=True)
    total_price = models.DecimalField(max_digits=7, decimal_places=2)
    condition_details = models.CharField(max_length=256)
    tracking_code = models.CharField(max_length=256)
    shipment_service = models.CharField(max_length=128)
    shipment_label = models.CharField(max_length=64)
    enabled = models.BooleanField(default=True)
    status = models.CharField(max_length=64)
    is_locked = models.BooleanField(default=False)
    serial_num = models.CharField(max_length=64)
    type = models.CharField(max_length=36)

    def __str__(self):
        return f"Purchase order #{self.uid}"


class SalesOrder(BaseModel):  
    translations = models.ManyToManyField(
        'account.Translation', 
        related_name="sales_orders"
    )  
    buyer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    debitor = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    invoice = models.ForeignKey(Invoice, on_delete=models.SET_NULL, null=True)
    user_owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True)
    services = models.ManyToManyField(ProductService, related_name="sale_orders")

    # serialized - serializer

    key = models.CharField(max_length=64)
    uid = models.CharField(max_length=64)
    note = models.TextField()
    cancellation = models.CharField(max_length=256)
    order_date = models.DateField(auto_now=True)
    total_price = models.DecimalField(max_digits=7, decimal_places=2)
    marketplace_price = models.DecimalField(max_digits=7, decimal_places=2)
    shipping_price = models.DecimalField(max_digits=7, decimal_places=2)
    marketplace = models.CharField(max_length=128)
    tracking_code = models.CharField(max_length=256)
    shipment_service = models.CharField(max_length=128)
    shipment_label = models.CharField(max_length=64)
    enabled = models.BooleanField(default=True)
    status = models.CharField(max_length=64)
    bookkeeping_status = models.CharField(max_length=64)
    is_locked = models.BooleanField(default=False)

    def __str__(self):
        return f"Sales order #{self.uid}"

class ProductUnit(BaseModel):
    product = models.ForeignKey(Product, related_name="items", on_delete=models.CASCADE)
    translations = models.ManyToManyField('account.Translation', related_name="serialized")
    purchase_order = models.ForeignKey(PurchaseOrder, related_name="serialized", on_delete=models.CASCADE)  
    sell_order = models.ForeignKey(SalesOrder, related_name="items", on_delete=models.SET_NULL, null=True)
    unit = models.ForeignKey(WarehouseStorage, related_name="prducts", on_delete=models.CASCADE)
    exp = models.ForeignKey(QualityData, related_name="serialized", on_delete=models.SET_NULL, null=True)
    user_owner = models.ForeignKey(User, related_name="zerialized", on_delete=models.SET_NULL, null=True)

    enabled = models.BooleanField(default=True)
    #num_items - serializer
    stock = models.DecimalField(max_digits=7, decimal_places=2)
    status = models.CharField(max_length=64)
    selling_price = models.DecimalField(max_digits=7, decimal_places=2)
    purchase_price = models.DecimalField(max_digits=7, decimal_places=2)
    vat = models.CharField(max_length=64)
    manufacturers_serial = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.vat} | {self.product.title}"