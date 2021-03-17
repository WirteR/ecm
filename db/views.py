from db.product.models import File
from db.serializers import FileSerializer
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet


class FileViewSet(GenericViewSet, CreateModelMixin, ListModelMixin):
    model_class = File
    queryset = model_class.objects.all()
    serializer_class = FileSerializer