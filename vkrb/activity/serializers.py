from django.contrib.contenttypes.models import ContentType
from django_serializer.serializer.base import ModelSerializer
from django_serializer.serializer.fields import SerializerField

from vkrb.activity.models import GiItem, SiItem
from vkrb.attachment.serializers import AttachmentSerializer
from vkrb.favorites.models import FavoriteItem


class ActivityGiItemSerializer(ModelSerializer):
    photo = SerializerField(source='get_photo')
    is_fav = SerializerField(source='get_fav')
    pdf = SerializerField(source='get_digest_pdf')
    is_actual =  SerializerField(source='get_is_actual')

    class Meta:
        model = GiItem
        exclude = ('photo_id', 'pdf_id', 'is_actual')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def get_photo(self, obj):
        return AttachmentSerializer(obj.photo).serialize()

    def get_fav(self, obj):
        content_type = ContentType.objects.get(model='giitem')
        if self.user.is_anonymous:
            return False
        is_fav = FavoriteItem.objects.filter(user=self.user, content_type=content_type, object_id=obj.id).exists()
        return is_fav

    def get_digest_pdf(self, obj):
        return AttachmentSerializer(obj.pdf).serialize()

    def get_is_actual(self, obj):
        return True if obj.is_actual else False


class ShortActivityGiItemSerializer(ModelSerializer):
    photo = SerializerField(source='get_photo')
    is_fav = SerializerField(source='get_fav')
    is_actual = SerializerField(source='get_is_actual')


    class Meta:
        model = GiItem
        exclude = ('photo_id', 'ceo', 'specialty',
                   'activity_course', 'history', 'contact_info',
                   'pdf_id', 'is_actual')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def get_fav(self, obj):
        content_type = ContentType.objects.get(model='giitem')
        if self.user.is_anonymous:
            return False
        is_fav = FavoriteItem.objects.filter(user=self.user, content_type=content_type, object_id=obj.id).exists()
        return is_fav

    def get_photo(self, obj):
        return AttachmentSerializer(obj.photo).serialize()

    def get_is_actual(self, obj):
        return True if obj.is_actual else False


class ActivitySiItemSerializer(ModelSerializer):
    photo = SerializerField(source='get_photo')
    is_fav = SerializerField(source='get_fav')
    pdf = SerializerField(source='get_digest_pdf')

    class Meta:
        model = SiItem
        exclude = ('photo_id', 'pdf_id')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def get_photo(self, obj):
        return AttachmentSerializer(obj.photo).serialize()

    def get_fav(self, obj):
        content_type = ContentType.objects.get(model='siitem')
        if self.user.is_anonymous:
            return False
        is_fav = FavoriteItem.objects.filter(user=self.user,
                                             content_type=content_type,
                                             object_id=obj.id).exists()
        return is_fav

    def get_digest_pdf(self, obj):
        return AttachmentSerializer(obj.pdf).serialize()


class ShortActivitySiItemSerializer(ModelSerializer):
    photo = SerializerField(source='get_photo')
    is_fav = SerializerField(source='get_fav')

    class Meta:
        model = SiItem
        exclude = ('photo_id', 'ceo', 'specialty',
                   'activity_course', 'history', 'contact_info',
                   'pdf_id')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def get_fav(self, obj):
        content_type = ContentType.objects.get(model='siitem')
        if self.user.is_anonymous:
            return False
        is_fav = FavoriteItem.objects.filter(user=self.user,
                                             content_type=content_type,
                                             object_id=obj.id).exists()
        return is_fav

    def get_photo(self, obj):
        return AttachmentSerializer(obj.photo).serialize()
