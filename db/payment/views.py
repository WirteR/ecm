from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.response import Response

from . import models as payment_models
from .serializers import PaymentSerializer, AccountSerializer, PaymentAccountSerializer
from db.helper_views import BaseModelsViewset, CustomQuerysetViewSet, CustomTrashViewSet
# Create your views here.

class PaymentViewSet(CustomTrashViewSet):
    model_class = payment_models.Payment
    queryset = model_class.objects.all()
    serializer_class = PaymentSerializer
        

class AccountViewSet(BaseModelsViewset, CustomQuerysetViewSet):
    model_class = payment_models.Account
    queryset = model_class.objects.all()
    serializer_class = AccountSerializer

    @action(methods=["get"], detail=False)
    def debitors(self, request):
        qs = super().get_queryset()
        ids = qs.prefetch_related("sale_orders").filter(sale_orders__isnull=False)\
                        .values_list("id", flat=True)
        qs = qs.filter(id__in=ids)
        return self.get_list(qs)
        
    @action(methods=["get"], detail=False)
    def creditors(self, request):
        qs = super().get_queryset()
        ids = qs.prefetch_related("purchase_orders").filter(purchase_orders__isnull=False)\
                        .values_list("id", flat=True)
        qs = qs.filter(id__in=ids)
        return self.get_list(qs)
    

class PaymentAccountViewSet(BaseModelsViewset):
    model_class = payment_models.PaymentAccount
    queryset = model_class.objects.all()
    serializer_class = PaymentAccountSerializer