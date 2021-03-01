from django.db import models

from db.account.models import Address, User
from db.core.models import BaseModel
from db.payment.models import Account, Payment
from db.product.models import Product, ProductService, QualityData
from db.warehouse.models import WarehouseStorage

# Create your models here.


class Invoice(BaseModel):
    translations = models.ManyToManyField(
        'account.Translation', 
        related_name="invoices",
        null=True,
        blank=True
    )
    url = models.FileField(upload_to="invoice")
    date = models.DateField(auto_now=True)
    num = models.CharField(max_length=128, unique=True)


class PurchaseOrder(BaseModel):
    seller = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="sellers")
    translations = models.ManyToManyField(
        'account.Translation', 
        related_name="purchase_orders"
    )
    creditor = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, related_name="purchase_orders")
    user_owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="purchase_orders")
    invoices = models.ManyToManyField(Invoice, blank=True, related_name="purchase_orders")
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, null=True, related_name="purchase_orders")

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
        related_name="sales_orders",
        blank=True
    )  
    buyer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="buyers")
    debitor = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, related_name="sale_orders")
    invoice = models.ForeignKey(Invoice, on_delete=models.SET_NULL, null=True, related_name="sale_orders")
    user_owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="sale_orders")
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True, related_name="sale_orders")
    services = models.ManyToManyField(ProductService, related_name="sale_orders", blank=True)

    # serialized - serializer

    key = models.CharField(max_length=64, null=True)
    uid = models.CharField(max_length=64)
    note = models.TextField()
    cancellation = models.CharField(max_length=256, null=True)
    order_date = models.DateField(auto_now=True)
    total_price = models.DecimalField(max_digits=7, decimal_places=2)
    marketplace_price = models.DecimalField(max_digits=7, decimal_places=2, default=0, null=True)
    shipping_price = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    marketplace = models.CharField(max_length=128, null=True)
    tracking_code = models.CharField(max_length=256, null=True)
    shipment_service = models.CharField(max_length=128, null=True)
    shipment_label = models.CharField(max_length=64, null=True)
    shipment_status = models.CharField(max_length=64, null=True)
    enabled = models.BooleanField(default=True)
    status = models.CharField(max_length=64)
    bookkeeping_status = models.CharField(max_length=64, null=True)
    is_locked = models.BooleanField(default=False)

    def __str__(self):
        return f"Sales order #{self.uid}"


class Tax(models.Model):
    tax_title = models.CharField(max_length=128)
    tax_description = models.TextField(null=True)
    tax_rate = models.DecimalField(max_digits=7, decimal_places=4, default=0, null=True)


class ProductUnit(BaseModel):
    product = models.ForeignKey(Product, related_name="items", on_delete=models.CASCADE)
    translations = models.ManyToManyField('account.Translation', related_name="serialized")
    purchase_order = models.ForeignKey(PurchaseOrder, related_name="serialized_products", on_delete=models.CASCADE, null=True)  
    sell_order = models.ForeignKey(SalesOrder, related_name="serialized_products", on_delete=models.SET_NULL, null=True)
    unit = models.ForeignKey(WarehouseStorage, related_name="products", on_delete=models.CASCADE, null=True)
    user_owner = models.ForeignKey(User, related_name="serialized", on_delete=models.SET_NULL, null=True)
    exp = models.ForeignKey(QualityData, on_delete=models.SET_NULL, null=True, blank=True)
    vat = models.ForeignKey(Tax, on_delete=models.SET_NULL, null=True)
    invoice_template = models.TextField(null=True) #make fk later
    enabled = models.BooleanField(default=True)
    serial_num = models.CharField(max_length=128, unique=True, default="")
    stock = models.DecimalField(max_digits=7, decimal_places=2)
    status = models.CharField(max_length=64)
    selling_price = models.DecimalField(max_digits=7, decimal_places=2)
    purchase_price = models.DecimalField(max_digits=7, decimal_places=2)
    manufacturers_serial = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.vat} | {self.product.title}"