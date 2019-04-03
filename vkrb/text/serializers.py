from django_serializer.serializer.base import ModelSerializer
from vkrb.text.models import Text


class TextSerializer(ModelSerializer):
    class Meta:
        model = Text
