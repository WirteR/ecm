from django.shortcuts import render

from .serializers import  OrderLogSerializer
from .models import OrderLog
from db.orders import OrderVars
from db.helper_views import BaseModelsViewset, CustomQuerysetViewSet
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from db.product.models import Product, ProductCategory
from db.product.serializers import ProductSerializer, ProductCategorySerializer
from db.orders.models import ProductUnit, PurchaseOrder, SalesOrder, Expense
from db.orders.serializers import ProductUnitSerializer, PurchaseOrderSerializer, SellingOrderSerializer, ExpenseSerializer
from db.payment.models import Payment
from db.payment.serializers import PaymentSerializer


class TrashViewSet(CustomQuerysetViewSet):

    @action(methods=["get"], detail=False)
    def restore_all(self, request):
        qs = super().get_queryset()
        qs.update(in_trash=False)
        return Response(data={"msg": "Restored!"})
    
    @action(methods=["get"], detail=False)
    def delete_all(self, request):
        qs = super().get_queryset()
        qs.delete()
        return Response(data={"msg": "Deleted!"})

    @action(methods=["get"], detail=False)
    def restore(self, request):
        ids = request.data.get("id", [])
        ids = json.loads(ids)
        qs = super().get_queryset()
        qs.filter(id__in=ids).update(in_trash=False)
        return Response(data={"msg": "Restored!"})
    
    @action(methods=["get"], detail=False)
    def delete(self, request):
        ids = request.data.get("id", [])
        ids = json.loads(ids)
        qs = super().get_queryset()
        qs.filter(id__in=ids).delete()
        return Response(data={"msg": "Deleted!"})


class ProductTrashViewSet(TrashViewSet):
    model_class = Product
    queryset = model_class.objects.filter(in_trash=True)
    serializer_class = ProductSerializer


class CategoriesTrashViewSet(TrashViewSet):
    model_class = ProductCategory
    queryset = model_class.objects.filter(in_trash=True)
    serializer_class = ProductCategorySerializer


class InventoryTrashViewSet(TrashViewSet):
    model_class = ProductUnit
    queryset = model_class.objects.filter(in_trash=True)
    serializer_class = ProductUnitSerializer


class PurchaseOrderTrashViewSet(TrashViewSet):
    model_class = PurchaseOrder
    queryset = model_class.objects.filter(in_trash=True)
    serializer_class = PurchaseOrderSerializer


class SellOrderTrashViewSet(TrashViewSet):
    model_class = SalesOrder
    queryset = model_class.objects.filter(in_trash=True)
    serializer_class = SellingOrderSerializer


class PaymentTrashViewSet(TrashViewSet):
    model_class = Payment
    queryset = model_class.objects.filter(in_trash=True)
    serializer_class = PaymentSerializer


class ExpenseTrashViewSet(TrashViewSet):
    model_class = Expense
    queryset = model_class.objects.filter(in_trash=True)
    serializer_class = ExpenseSerializer


class PurchaseOrderLogViewSet(BaseModelsViewset):
    model_class = PurchaseOrder
    queryset = model_class.objects.all()
    serializer_class = PurchaseOrderSerializer



class SellOrderLogView(BaseModelsViewset):
    model_class = SalesOrder
    queryset = model_class.objects.all()
    serializer_class = SellingOrderSerializer
    filter_backends = []



# class OrderLogViewSet(CustomQuerysetViewSet):
#     model_class = OrderLog
#     queryset = model_class.objects.all()
#     serializer_class = OrderLogSerializer

#     @action(methods=["get"], detail=False)
#     def order_purchases(self, request):
#         qs = super().get_queryset()
#         qs = qs.filter(order_type=OrderVars.PURCHASE_ORDER)
#         return self.get_list(qs)

#     @action(methods=["get"], detail=False)
#     def order_sales(self, request):
#         qs = super().get_queryset()
#         qs = qs.filter(order_type=OrderVars.SELL_ORDER)
#         return self.get_list(qs)  