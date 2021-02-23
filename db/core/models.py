from django.db import models
from django.db import connection


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
 
    class Meta:
        abstract = True


class Tenant(BaseModel):
    company_name = models.CharField(max_length=128, unique=True)
    paid_until =  models.DateField(auto_now=True)
    on_trial = models.BooleanField(default=True)
    db_conf = models.JSONField()
    db_name = models.CharField(max_length=128)

    def __str__(self):
        return self.company_name

    def delete(self):
        with connection.cursor() as cursor:
            cursor.execute(f"DROP SCHEMA IF EXISTS {self.db_name}_schema CASCADE;")




