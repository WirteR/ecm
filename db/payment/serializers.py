from rest_framework.serializers import ModelSerializer

from . import models as payment_models


class AccountSerializer(ModelSerializer):
    class Meta:
        model = payment_models.Account
        fields = "__all__"


class PaymentSerializer(ModelSerializer):
    class Meta:
        models = payment_models.Payment
        fields = "__all__"