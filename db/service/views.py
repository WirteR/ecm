from django.shortcuts import render

from . import serializers as service_serializer
from . import models as service_models
from db.core.views import BaseModelsViewset


class ExpenseFileViewSet(BaseModelsViewset):
    model_class = service_models.ExpenseFile
    queryset = model_class.objects.all()
    serializer_class = service_serializer.ExpenseFileSerializer
    

class ExpenseSupplierViewSet(BaseModelsViewset):
    model_class = service_models.ExpenseSupplier
    queryset = model_class.objects.all()
    serializer_class = service_serializer.ExpesnseSupplierSerializer


class ExpenseCategoryViewSet(BaseModelsViewset):
    model_class = service_models.ExpenseCategory
    queryset = model_class.objects.all()
    serializer_class = service_serializer.ExpenseCategorySerializer


class ExpenseViewSet(BaseModelsViewset):
    model_class = service_models.Expense
    queryset = model_class.objects.all()
    serializer_class = service_serializer.ExpenseSerializer


class ExpenseItemViewSet(BaseModelsViewset):
    model_class = service_models.ExpenseItem
    queryset = model_class.objects.all()
    serializer_class = service_serializer.ExpenseItemSerializer