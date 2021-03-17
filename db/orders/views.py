from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from . import models as order_models
from . import serializers as order_serializers
from db.helper_views import BaseModelsViewset, CustomQuerysetViewSet, CustomTrashViewSet
from db.filters import ConditionFilter, DateFilter, EdgeDateFilter, PermissionFilter
from db.permissions import CustomPermission
from . import OrderVars, ExpenseVars
from db.uploads import start_upload
# Create your views here.

class InvoiceViewSet(ModelViewSet):
    model_class = order_models.Invoice
    queryset = model_class.objects.all()
    serializer_class = order_serializers.PurchaseInvoiceSerializer
    

class SerializedViewSet(CustomTrashViewSet):
    model_class = order_models.ProductUnit
    queryset = model_class.objects.all()
    serializer_class = order_serializers.ProductUnitSerializer


class PurchaseViewSet(CustomTrashViewSet):
    permission_classes = [CustomPermission]
    filter_backends = [ConditionFilter, DateFilter, EdgeDateFilter, PermissionFilter]
    date_filter_field = "created_at"
    filter_fields = ["uid", "condition", "tracking_code", "total_price", "created_at"]
    model_class = order_models.PurchaseOrder
    queryset = model_class.objects.all()
    serializer_class = order_serializers.PurchaseOrderSerializer

    @action(methods=["post"], detail=False)
    def upload_csv(self, request):
        start_upload(self.model_class, request)
    

class SalesOrderViewSet(CustomTrashViewSet):
    model_class = order_models.SalesOrder
    queryset = model_class.objects.all()
    serializer_class = order_serializers.SellingOrderSerializer


class ExpenseSupplierViewSet(BaseModelsViewset):
    model_class = order_models.ExpenseSupplier
    queryset = model_class.objects.all()
    serializer_class = order_serializers.ExpenseSupplierSerializer


class ExpenseViewSet(CustomTrashViewSet):
    model_class = order_models.Expense
    queryset = model_class.objects.all()
    serializer_class = order_serializers.ExpenseSerializer


class ExpenseItemViewSet(BaseModelsViewset):
    model_class = order_models.ExpenseItem
    queryset = model_class.objects.all()
    serializer_class = order_serializers.ExpenseItemSerializer