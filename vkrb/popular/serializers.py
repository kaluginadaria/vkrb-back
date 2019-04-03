from django_serializer.serializer.base import ModelSerializer
from vkrb.popular.models import UserPopular


class UserPopularSerializer(ModelSerializer):
    class Meta:
        model = UserPopular
        exclude = ('user_id', )
