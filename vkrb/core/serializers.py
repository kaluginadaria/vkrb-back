from django_serializer.serializer.base import ModelSerializer
from django_serializer.serializer.fields import SerializerField

from vkrb.attachment.serializers import AttachmentSerializer
from vkrb.core.models import User, PushToken


class UserSerializer(ModelSerializer):
    photo = SerializerField(source='get_photo')

    class Meta:
        model = User
        exclude = (
            'is_staff', 'is_superuser', 'password',
            'date_joined', 'last_login', 'photo_id'
        )

    def get_photo(self, obj):
        return AttachmentSerializer(obj.photo).serialize()


class PushTokenSerializer(ModelSerializer):
    class Meta:
        model = PushToken
        exclude = ('session_key',)
