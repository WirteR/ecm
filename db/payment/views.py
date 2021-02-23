from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.response import Response

from . import models as payment_models
from .serializers import PaymentSerializer, AccountSerializer
from db.core.views import BaseModelsViewset
# Create your views here.

class Payment(BaseModelsViewset):
    model_class = payment_models.Payment
    queryset = payment_models.objects.all()
    serializer_class = PaymentSerializer


class Account(BaseModelsViewset):
    model_class = payment_models.Account
    queryset = model_class.objects.all()
    serializer_class = AccountSerializer

    def get_list(self, queryset):
        page = self.paginate_queryset(queryset)
        if page is not None: 
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=["get"], detail=False)
    def debitors(self, request):
        qs = super().get_queryset()
        ids = qs.objects.prefetch_related("sale_orders").filter(sale_orders__isnull=False)\
                        .values_list("id", flat=True)
        qs = qs.filter(id__in=ids)
        return self.get_list(qs)
        
    @action(methods=["get"], detail=False)
    def creditors(self, request):
        qs = super().get_queryset()
        ids = qs.objects.prefetch_related("purchase_orders").filter(purchase_orders__isnull=False)\
                        .values_list("id", flat=True)
        qs = qs.filter(id__in=ids)
        return self.get_list(qs)
    

