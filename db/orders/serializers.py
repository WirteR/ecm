from rest_framework import serializers
from django.core.files.storage import default_storage

from db.helper_serializers import BaseTranslateSerializer
from db.payment.serializers import AccountSerializer, PaymentSerializer
from db.payment.models import Payment
from db.product.models import QualityData
from db.product.serializers import ProductSerializer, QualityDataSerializer
from db.account.serializers import CustomerSerializer
from db.local_settings.serializers import TaxSerializer
from db.serializers import FileSerializer
from db.utils import write_instance
# from .serializers import ProductUnitSerializer

from . import models as order_models


class InvoiceSerializer(BaseTranslateSerializer):
    file = FileSerializer(many=False, read_only=True)
    file_id = serializers.IntegerField()

    class Meta:
        model = order_models.Invoice
        fields = [
            "id",
            "num",
            "date",
            "file",
            "file_id",
            "translations"
        ]


class ReadOnlySalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = order_models.SalesOrder
        fields = "__all__"


class SaleInvoiceSerializer(BaseTranslateSerializer):
    order = ReadOnlySalesSerializer(required=False, write_only=True)
    file = FileSerializer(many=False)
    class Meta:
        model = order_models.Invoice
        fields = [
            "id",
            "file",
            "order",
            "date",
            "num",
            "translations"
        ]
        read_only_fields = ['id', "url"]

    def save(self):
        file = self.generate_invoice()
        self.validated_data["url"] = file
        return super().save()

    def generate_invoice(self):
        if order_data := self.validated_data.get("order"):
            self.validated_data.pop("order")
        else:
            return
        return


class PurchaseInvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = order_models.Invoice
        fields = "__all__"


class ProductUnitSerializer(BaseTranslateSerializer):
    product = ProductSerializer(many=False, required=False, read_only=True)
    exp = QualityDataSerializer(many=False, required=False)

    vat = TaxSerializer(many=False, read_only=True)
    vat_id = serializers.IntegerField(required=False, allow_null=True)

    product_id = serializers.IntegerField(required=True)
    purchase_order = serializers.PrimaryKeyRelatedField(
        required=False, 
        queryset=order_models.PurchaseOrder.objects.all()
    )

    class Meta:
        model = order_models.ProductUnit
        fields = [
            "id",
            "serial_num",
            "status",
            "stock",
            "enabled",
            "manufacturers_serial",
            "selling_price",
            "purchase_price",
            "created_at",
            "exp",
            "vat",
            "vat_id",
            'product',
            "product_id",
            "sell_order",
            "sell_order_id",
            "purchase_order",
            "user_owner"
        ]
        read_only_fields = ["user_owner"]
        write_only_fields = ["product_id", "vat_id"]

    def save(self):
        exp = self.validated_data.pop("exp", [])
        instance = super().save()

        if exp:
            exp_instance = write_instance(data=exp, serializer_class=QualityDataSerializer)
            instance.exp = exp_instance

        instance.user_owner = self.context["request"].user.id
        return instance.save()


class UpdateProductUnitSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=True, write_only=True)
    sell_order_id = serializers.IntegerField(required=False, write_only=True)
    class Meta:
        model = order_models.ProductUnit
        fields = [
            "id",
            "serial_num",
            "selling_price",
            "invoice_template",
            "sell_order_id",
            "vat_id"
        ]
        write_only = "__all__"

    def update(self):
        product = order_models.ProductUnit.objects.filter(id=self.validated_data["id"])
        product.update(**self.validated_data)
        return product

                
class SellingOrderSerializer(BaseTranslateSerializer):
    buyer = CustomerSerializer(required=False)
    buyer_id = serializers.CharField(required=False, write_only=True)
    debitor = AccountSerializer(read_only=True)
    debitor_id = serializers.IntegerField(required=False, write_only=True)
    payment = PaymentSerializer(read_only=True)
    payment_id = serializers.IntegerField(required=False, write_only=True)
    invoice = SaleInvoiceSerializer(many=False)
    serialized_products = ProductUnitSerializer(many=True, read_only=True)
    products = UpdateProductUnitSerializer(many=True, write_only=True, required=True)
    
    class Meta:
        model = order_models.SalesOrder
        fields = [
            "id",
            "uid",
            "status",
            "bookkeeping_status",
            "marketplace",
            "note", 
            "total_price", 
            "shipment_status",
            "tracking_code", 
            "buyer", 
            "buyer_id", 
            "debitor",
            "debitor_id",
            "payment",
            "payment_id",
            "invoice",
            "serialized_products",
            "products",
            "user_owner"
        ]
        read_only_fields = ["user_owner"]

    def save(self):
        if buyer := self.validated_data.get("buyer"):
            self.validated_data.pop("buyer")
        if serialized := self.validated_data.get("products", []):
            self.validated_data.pop("products")
        if invoice := self.validated_data.get("invoice"):
            self.validated_data.pop("invoice")
        
        instance = super().save()

        if serialized:
            for product in serialized:
                product["sell_order_id"] = instance.id
                serializer = UpdateProductUnitSerializer(data=product)
                serializer.is_valid()
                serializer.update()
                
        if buyer:
            buyer_instance = write_instance(data=buyer, serializer_class=CustomerSerializer)
            instance.buyer = buyer_instance
        
        if invoice:
            invoice["order"] = ReadOnlySalesSerializer(instance).data
            serializer = SaleInvoiceSerializer(data=invoice)
            serializer.is_valid()
            instance.invoice = serializer.save()
        
        instance.user_owner = self.context["request"].user.id
        return instance.save()
    

class PurchaseOrderSerializer(BaseTranslateSerializer):
    seller = CustomerSerializer(required=False)
    seller_id = serializers.CharField(required=False, allow_null=True)
    creditor = AccountSerializer(required=False, read_only=True)
    creditor_id = serializers.IntegerField(required=False)
    payment = PaymentSerializer(required=False, read_only=True)
    payment_id = serializers.IntegerField(required=False, allow_null=True)
    serialized_products = ProductUnitSerializer(many=True, required=False)
    invoices = serializers.SerializerMethodField(read_only=True)
    invoice_ids = serializers.ListField(child=serializers.IntegerField(), required=False, write_only=True, allow_null=True)

    class Meta:
        model = order_models.PurchaseOrder
        fields = [
            "id",
            "uid",
            "is_locked",
            "total_price",
            "status", 
            "tracking_code",
            "condition_details",
            "order_date",
            "created_at", 
            "updated_at",
            "seller",
            "seller_id",
            "creditor",
            "creditor_id",
            "payment",
            "payment_id",
            "serialized_products",
            "translations",
            "invoices",
            "invoice_ids",
            "user_owner"
        ]
        read_only_fields = ["user_owner"]
        write_only_fields = ["payment_id", "creditor_id", "seller_id"]

    def get_invoices(self, obj):
        qs = obj.invoices.all()
        ls = [default_storage.url(str(obj.file)) for obj in qs]
        return   

    def save(self):
        seller = self.validated_data.pop("seller", {})
        invoice_ids = self.validated_data.pop("invoice_ids", [])
        serialized = self.validated_data.pop("serialized_products", [])
        instance = super().save()

        if invoice_ids:
            instance.invoices.add(*invoice_ids)
        if serialized:
            for pu in serialized:
                pu["purchase_order"] = instance.id
                product_serializer = ProductUnitSerializer(data=pu, context=self.context)
                product_serializer.is_valid()
                product_serializer.save()

        if seller:
            seller_instance = write_instance(data=seller, serializer_class=CustomerSerializer, context=self.context)
            instance.seller = seller_instance
        
        instance.user_owner = self.context["request"].user.id
        return instance.save()


class ExpenseSupplierSerializer(BaseTranslateSerializer):
    account = serializers.StringRelatedField(many=False, read_only=True)
    account_id = serializers.IntegerField()

    class Meta:
        model = order_models.ExpenseSupplier
        fields = [
            "id",
            "company_name",
            "zip",
            "street",
            "city",
            "country",
            "tax_id",
            "account",
            "account_id",
            "updated_at",
            "created_at",
            "translations",
        ]


class ExpenseItemSerializer(BaseTranslateSerializer):
    account_id = serializers.IntegerField()
    expense_id = serializers.IntegerField(required=False)

    class Meta:
        model = order_models.ExpenseItem
        fields = [
            "id",
            "amount",
            "description",
            "var_percent",
            "vat",
            "expense_id",
            "account_id",
        ]


class ExpenseSerializer(BaseTranslateSerializer):
    payment = serializers.PrimaryKeyRelatedField(allow_null=True, queryset=Payment.objects.all())
    supplier = serializers.PrimaryKeyRelatedField(queryset=order_models.ExpenseSupplier.objects.all())
    invoice = InvoiceSerializer()
    expense_items = ExpenseItemSerializer(many=True, required=False)

    class Meta:
        model = order_models.Expense
        fields = [
            "uid",
            "total_price",
            "bookkeeping_status",
            "date",
            "supplier",
            "payment",
            "expense_items",
            "invoice",
            "translations",
            "user_owner"
        ]     
        read_only_fields = ["user_owner"]   

    def save(self):
        if invoice := self.validated_data.get("invoice"):
            self.validated_data.pop("invoice")
        if items := self.validated_data.get("expense_items"):
            self.validated_data.pop("expense_items")
        
        instance = super().save()

        if invoice:
            invoice_instance = write_instance(data=invoice, serializer_class=InvoiceSerializer)
            instance.invoice_id = invoice_instance.id
        if items:
            write_instance(
                data=items, 
                serializer_class=ExpenseItemSerializer, 
                many=True, 
                extra_field="expense_id", 
                extra_field_value=instance.id
            )
        instance.user_owner = self.context["request"].user.id
        return instance.save()