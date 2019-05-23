from django.contrib.contenttypes.models import ContentType
from django_serializer.serializer.base import ModelSerializer
from django_serializer.serializer.fields import SerializerField

from vkrb.core.serializers import UserSerializer
from vkrb.favorites.models import FavoriteItem
from vkrb.recourse.models import Recourse


class RecourseSerializer(ModelSerializer):
    children = SerializerField(source='get_childs')
    # favs = SerializerField(source='get_likes')
    user = SerializerField(source='get_owner')
    is_fav = SerializerField(source='get_fav')

    class Meta:
        model = Recourse
        exclude = ('user', 'user_id')

    def __init__(self, *args, **kwargs):
        self.request_user = kwargs.pop('request_user')
        super().__init__(*args, **kwargs)

    def get_owner(self, obj):
        user = obj.user
        return UserSerializer(user).serialize()

    def get_childs(self, obj):
        if obj.parent is None:
            children = Recourse.objects.filter(parent=obj).order_by('created')
            return RecourseSerializer(
                children,
                multiple=True,
                request_user=self.request_user
            ).serialize()

    def get_fav(self, obj):
        content_type = ContentType.objects.get(model='recourse')
        is_fav = FavoriteItem.objects.filter(user=self.request_user,
                                             content_type=content_type,
                                             object_id=obj.id).exists()
        return is_fav
