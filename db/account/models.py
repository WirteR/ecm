from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from db.core.models import BaseModel
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

class Translation(models.Model):
    lang = models.CharField(max_length=24)
    title = models.CharField(max_length=128)
    description = models.TextField()


class Address(BaseModel):
    street = models.CharField(max_length=256)
    street_number = models.CharField(max_length=16, blank=True, default=True)
    zip = models.CharField(max_length=24)
    city = models.CharField(max_length=64)
    country = models.CharField(max_length=64, blank=True, default="")
    key = models.CharField(max_length=128, null=True, blank=True)
    location_name = models.CharField(max_length=128, null=True, blank=True)
    location_ID = models.CharField(max_length=64, null=True, blank=True)

    def __str__(self):
        return f"{self.country} -> {self.city} -> {self.street} -> {self.street_number}" 


class User(AbstractUser):
    tenant_id = models.IntegerField(null=True)
    status = models.CharField(max_length=128)
    avatar = models.ImageField(upload_to="user-avatars")
    lang = models.CharField(max_length=16, default="en-GB")

    phone = models.CharField(max_length=24)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    account = models.CharField(max_length=128, null=True)
    roles = models.CharField(max_length=48, default="")
    name = models.CharField(max_length=128, null=True)
    def __str__(self):
        return self.username
 
    def save(self, force_insert=False, force_update=False, request=None, *args, **kwargs):
        if request:
            self.tenant_id = request.tenant_id
        super().save(force_insert, force_update, *args, **kwargs)
        

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance) 