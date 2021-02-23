from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet
from . import models as order_models
from . import serializers as order_serializers
from db.core.views import BaseModelsViewset
# Create your views here.

class Invoice(ModelViewSet):
    model_class = order_models.Invoice
    queryset = model_class.objects.all()
    serializer_class = order_serializers.InvoiceSerializer
    

class SerializedViewSet(BaseModelsViewset):
    model_class = order_models.ProductUnit
    queryset = model_class.objects.all()
    serializer_class = order_serializers.ProductUnitSerializer


class PurchaseViewSet(BaseModelsViewset):
    model_class = order_models.PurchaseOrder
    queryset = model_class.objects.all()
    serializer_class = order_serializers.PurchaseOrderSerializer
    
    def get_queryset(self):
        qs = super().get_queryset().prefetch_related("serialized_products")
        return qs


class SalesOrder(BaseModelsViewset):
    model_class = order_models.SalesOrder
    queryset = model_class.objects.all()
    serializer_class = order_serializers.SellingOrderSerializer

    def get_queryset(self):
        qs = super().get_queryset().prefetch_related("serialized_products")
        return qs
