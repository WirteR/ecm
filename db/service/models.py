from django.db import models
from db.orders import OrderVars
from db.helper_models import BaseModel

class OrderLog(BaseModel):
    order_type = models.CharField(max_length=128, choices=OrderVars.LOG_TYPES)
    data = models.JSONField()