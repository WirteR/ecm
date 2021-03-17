from django.shortcuts import render
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from db.settings import models as settings_models 
from db.settings import serializers as settings_serializers
from db.helper_views import BaseSettingsView


# Create your views here.

class BaseSettingsLangView(BaseSettingsView):

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(tenant_id=self.request.tenant_id)
    
    def get_filtered_queryset(self):
        qs = super().get_filtered_queryset()
        lang = self.request.data.get("lang")
        return qs.filter(lang=lang)


class CompanySettingsViewset(BaseSettingsView):
    model_class = settings_models.CompanySettings
    queryset = model_class.objects.all()
    serializer_class = settings_serializers.CompanySettingSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(tenant_id=self.request.tenant_id)

    
class SMTPViewset(BaseSettingsView):
    model_class = settings_models.SMTP
    queryset = model_class.objects.all()
    serializer_class = settings_serializers.SMTPSerializer
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(tenant_id=self.request.tenant_id)


class PurchaseOrderViewset(BaseSettingsLangView):
    model_class = settings_models.PurchaseOrderSettings
    queryset = model_class.objects.all()
    serializer_class = settings_serializers.PurchaseOrderSettingsSerializer


class SalesOrderViewset(BaseSettingsLangView):
    model_class = settings_models.SalesOrderSettings
    queryset = model_class.objects.all()
    serializer_class = settings_serializers.SalesOrderSettingsSerializer


class ImageSettingViewset(BaseSettingsView):
    model_class = settings_models.ImageSettings
    queryset = model_class.objects.all()
    serializer_class = settings_serializers.ImageSettingsSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(tenant_id=self.request.tenant_id)


class ShopSettingViewset(BaseSettingsLangView):
    model_class = settings_models.ShopSettings
    queryset = model_class.objects.all()
    serializer_class = settings_serializers.ShopSettingsSerializer


class ShopStylingViewset(BaseSettingsView):
    model_class = settings_models.ShopStyling
    queryset = model_class.objects.all()
    serializer_class = settings_serializers.ShopStylingSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(tenant_id=self.request.tenant_id)


class ShopNewsletterViewset(BaseSettingsLangView):
    model_class = settings_models.ShopNewsletter
    queryset = model_class.objects.all()
    serializer_class = settings_serializers.ShopNewsletterSerializer


class UIDViewset(BaseSettingsView):
    model_class = settings_models.UID
    queryset = model_class.objects.all()
    serializer_class = settings_serializers.UIDSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(tenant_id=self.request.tenant_id)


class HeaderViewset(BaseSettingsView):
    model_class = settings_models.HeaderSettings
    queryset = model_class.objects.all()
    serializer_class = settings_serializers.HeaderSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(tenant_id=self.request.tenant_id)