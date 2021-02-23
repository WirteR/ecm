from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from db.account.models import Translation
from db.account.serializers import TranslationSerializer


class DefaultPagination(PageNumberPagination):
    page_size = 200
    page_size_query_param = "perPage"
    max_page_size = 1000


class ExtendViewset(viewsets.ViewSet):
    @property
    def client(self):
        return self.request.client


class BaseModelsViewset(viewsets.ModelViewSet):
    pagination_class = DefaultPagination

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.prefetch_related("translations")

    @action(methods=["post"], detail=True)
    def set_translation(self, request, pk=None):
        obj = self.get_object()
        serializer = TranslationSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(status=300, data={"message: Passed data is not valid"})

        
        obj.translations.update_or_create(**serializer.data)
        return Response(status=200, data={"message": "Translation created"})

    @action(methods=["post"], detail=True)
    def delete_translation(self, request, pk=None):
        obj = self.get_object()
        translation_id = request.query_params.get("translation_id", None)
        print(translation_id)
        try:
            translation = Translation.objects.get(id=translation_id)
            translation.delete()
            return Response(status=200, data={"message": "Translation was delete succesfully"})
        except:
            return Response(status=404, data={"message": "Translation not found"}) 