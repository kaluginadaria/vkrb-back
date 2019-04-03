from django.contrib.contenttypes.models import ContentType
from django_serializer.serializer.base import ModelSerializer
from django_serializer.serializer.fields import SerializerField

from vkrb.attachment.serializers import AttachmentSerializer
from vkrb.calc.models import Formula
from vkrb.calc.utils import FORMULAS
from vkrb.favorites.models import FavoriteItem


class FormulaSerializer(ModelSerializer):
    photo = SerializerField(source='get_image')
    is_fav = SerializerField(source='get_fav')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    class Meta:
        model = Formula
        exclude = ('photo_id',)

    def get_image(self, obj):
        return AttachmentSerializer(obj.photo).serialize()

    def _serialize_obj(self, obj):
        result = super()._serialize_obj(obj)
        key = result.get('key')
        try:
            params = dict(FORMULAS.get(key))
            result.update({'params': params})
        except TypeError:
            pass

        return result

    def get_fav(self, obj):
        content_type = ContentType.objects.get(model='formula')
        is_fav = FavoriteItem.objects.filter(user=self.user,
                                             content_type=content_type,
                                             object_id=obj.id).exists()
        return is_fav
