from django.db import models

from db.core.models import BaseModel, User


class Translation(models.Model):
    lang = models.CharField(max_length=24)
    title = models.CharField(max_length=128)
    description = models.TextField()


class Address(BaseModel):
    street = models.CharField(max_length=256)
    street_number = models.CharField(max_length=16)
    zip = models.CharField(max_length=24)
    city = models.CharField(max_length=64)
    country = models.CharField(max_length=64)
    key = models.CharField(max_length=128)
    location_name = models.CharField(max_length=128)
    location_ID = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.country} -> {self.city} -> {self.street} -> {self.street_number}" 


class Customer(models.Model):
    phone = models.CharField(max_length=24)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    customer = models.OneToOneField(User, on_delete=models.CASCADE, related_name="customer")
    roles = models.CharField(max_length=48)

    def __str__(self):
        return self.phone