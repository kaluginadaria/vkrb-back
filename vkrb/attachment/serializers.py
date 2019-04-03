from django_serializer.serializer.base import ModelSerializer
from django_serializer.serializer.fields import SerializerField

from vkrb.attachment.models import Attachment
from vkrb.core.utils import build_url
from vkrb.newsitem.models import NewsItem


class AttachmentSerializer(ModelSerializer):
    url = SerializerField(source='get_url')

    class Meta:
        model = Attachment
        exclude = ('file', 'created')

    def get_url(self, obj):
        return build_url(obj.file.url)
