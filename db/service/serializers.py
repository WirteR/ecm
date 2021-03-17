from rest_framework import serializers
from .models import OrderLog
import json


class OrderLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderLog
        fields = [
            "data"
        ]

    def to_representation(self, obj):
        data = super().to_representation(obj)
        data = json.loads(data["data"])
        return data

