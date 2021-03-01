from rest_framework.serializers import Serializer

from . import models as service_models
from db.core.serializers import BaseTranslateSerializer


class ExpenseFileSerializer(Serializer):
    pass


class ExpesnseSupplierSerializer(Serializer):
    pass


class ExpenseCategorySerializer(Serializer):
    pass


class ExpenseSerializer(Serializer):
    pass


class ExpenseItemSerializer(Serializer):
    pass