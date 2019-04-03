from django.contrib.contenttypes.models import ContentType
from django_serializer.serializer.base import ModelSerializer
from django_serializer.serializer.fields import SerializerField

from vkrb.activity.models import SiItem
from vkrb.activity.serializers import ActivitySiItemSerializer
from vkrb.attachment.serializers import AttachmentSerializer
from vkrb.expert.models import Expert
from vkrb.favorites.models import FavoriteItem



class ExpertSerializer(ModelSerializer):
    photo = SerializerField(source='get_avatar')
    is_fav = SerializerField(source='get_fav')
    si = SerializerField(source='get_si')
    specialty = SerializerField(source='get_specialty')
    class Meta:
        model = Expert
        exclude = ('photo_id', 'si_id', 'gi_id','specialty_id')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def get_avatar(self, obj):
        return AttachmentSerializer(obj.photo).serialize()

    def get_fav(self, obj):
        content_type = ContentType.objects.get(model='expert')
        is_fav = FavoriteItem.objects.filter(user=self.user,
                                             content_type=content_type,
                                             object_id=obj.id).exists()
        return is_fav

    def get_si(self, obj):

        return ActivitySiItemSerializer(obj.si, user=self.user).serialize()

    def get_specialty(self, obj):
        from vkrb.recourse.serializers import SpecialtySerializer
        return SpecialtySerializer(obj.specialty).serialize()
