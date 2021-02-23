from django.shortcuts import render

from db.core.views import BaseModelsViewset
from .models import Warehouse
from .serializers import WarehouseSerializer


class WarehouseViewSet(BaseModelsViewset):
    model_class = Warehouse
    queryset = model_class.objects.all()
    serializer_class = WarehouseSerializer
    

