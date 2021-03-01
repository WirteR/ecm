from rest_framework import serializers
from django.core.files.storage import default_storage

from db.core.serializers import BaseTranslateSerializer
from db.payment.serializers import AccountSerializer, PaymentSerializer
from db.product.models import QualityData
from db.product.serializers import ProductSerializer, QualityDataSerializer
from db.account.serializers import UserSerializer, CustomerSerializer
# from .serializers import ProductUnitSerializer

from . import models as order_models

class ReadOnlySalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = order_models.SalesOrder
        fields = "__all__"


class SaleInvoiceSerializer(serializers.ModelSerializer):
    order = ReadOnlySalesSerializer(required=False, write_only=True)
    class Meta:
        model = order_models.Invoice
        fields = [
            "id",
            "url",
            "order",
            "date",
            "num"
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


class TaxSerializer(serializers.ModelSerializer):
    class Meta:
        model = order_models.Tax
        fields = "__all__"


class ProductUnitSerializer(BaseTranslateSerializer):
    product = ProductSerializer(many=False, required=False)
    exp = QualityDataSerializer(many=False, required=False)

    vat = TaxSerializer(many=False, read_only=True)
    vat_id = serializers.IntegerField(required=False, write_only=True)

    product_id = serializers.IntegerField(required=True)
    purchase_order_id = serializers.IntegerField(required=False)

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
            "purchase_order_id"
        ]
        write_only_fields = ["product_id", "purchase_order_id"]

    def save(self):
        if exp := self.validated_data.get("exp", []):
            exp = self.validated_data.pop("exp")

        instance = super().save()

        if exp:
            serializer = QualityDataSerializer(data=exp)
            serializer.is_valid()
            exp_instance = serializer.save()
            instance.exp_id = exp_instance.id

        return instance


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
    buyer_id = serializers.IntegerField(required=False, write_only=True)
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
            "products"
        ]

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
            serializer = CustomerSerializer(data=buyer)
            serializer.is_valid()
            instance.buyer = serializer.save()
        
        if invoice:
            invoice["order"] = ReadOnlySalesSerializer(instance).data
            serializer = SaleInvoiceSerializer(data=invoice)
            serializer.is_valid()
            instance.invoice = serializer.save()
        
        return instance.save()
    

class PurchaseOrderSerializer(BaseTranslateSerializer):
    seller = CustomerSerializer(required=False)
    seller_id = serializers.IntegerField(required=True)
    creditor = AccountSerializer(required=False, read_only=True)
    creditor_id = serializers.IntegerField(required=False)
    payment = PaymentSerializer(required=False, read_only=True)
    payment_id = serializers.IntegerField(required=False)
    serialized_products = ProductUnitSerializer(many=True, required=False)
    invoice = serializers.SerializerMethodField(read_only=True, required=False)
    invoice_id = serializers.ListField(child=serializers.IntegerField(), required=False, write_only=True)

    #TODO user_owner

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
            "invoice_urls",
            "invoice_ids"   
        ]
        write_only_fields = ["payment_id", "creditor_id", "seller_id"]

    def get_invoice_urls(self, obj):
        qs = obj.invoices.all()
        ls = [default_storage.url(str(obj.image)) for obj in qs]
        return   

    def save(self):
        if seller := self.validated_data.get("seller", {}):
            seller = self.validated_data.pop("seller")
        if invoice_ids := self.validated_data.get("invoice_ids", []):
            invoice_ids = self.validated_data.pop("invoice_ids")
        if serialized := self.validated_data.get("serialized_products"):
            serialized = self.validated_data.pop("serialized_products")
        
        instance = super().save()

        if invoice_ids:
            instance.add(*invoice_ids)
        if serialized:
            for pu in serialized:
                pu["purchase_order_id"] = instance.id
                product_serializer = ProductUnitSerializer(data=pu)
                product_serializer.is_valid()
                product_serializer.save()
        if seller:
            serializer = CustomerSerializer(data=seller)
            serializer.is_valid()
            seller_instance = serializer.save()
            instance.seller = seller_instance

        instance.save()
        return instance
        

    def clear_data(self):
        model_fields = self.Meta.model._meta.fields
        for x in self.validated_data.keys():
            if x not in model_fields:
                self.validated_data.pop(x)