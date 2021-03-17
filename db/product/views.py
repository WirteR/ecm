from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
import simplejson as json

from db.helper_views import BaseModelsViewset, CustomTrashViewSet
from db.filters import ConditionFilter

from . import models as product_models
from db.account.models import Translation

from . import serializers as product_serializers


class CategoryViewSet(CustomTrashViewSet):
    filter_backends = [OrderingFilter]    
    ordering_fields = ["uid", "name", "created_at"]
    model_class = product_models.ProductCategory
    serializer_class = product_serializers.ProductCategorySerializer
    queryset = model_class.objects.all()

    
class AttributeViewSet(BaseModelsViewset):
    model_class = product_models.ProductAttribute
    serializer_class = product_serializers.AttributeSerializer
    queryset = model_class.objects.all()
        

class TagViewSet(BaseModelsViewset):
    serializer_class = product_serializers.TagSerializer
    model_class = product_models.ProductTag
    queryset = model_class.objects.all()


class ProductViewSet(CustomTrashViewSet):
    serializer_class = product_serializers.ProductSerializer
    models_class = product_models.Product
    queryset = models_class.objects.all()


class ProductServiceViewSet(BaseModelsViewset):
    serializer_class = product_serializers.ProductServiceSerializer
    model_class = product_models.ProductService
    queryset = model_class.objects.all()