from django_serializer.serializer.base import ModelSerializer

from vkrb.user.models import UserChanged


class UserChangedSerializer(ModelSerializer):
    class Meta:
        model = UserChanged
        exclude = (
            'status', 'reason', 'created_date',
            'is_status_set','id'
        )
