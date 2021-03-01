from rest_framework.serializers import ModelSerializer
from db.account.serializers import TranslationSerializer


class BaseTranslateSerializer(ModelSerializer):
    translations = TranslationSerializer(many=True, required=False, read_only=True)