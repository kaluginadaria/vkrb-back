from django.contrib.contenttypes.models import ContentType
from django.db.models import Count
from django_serializer.serializer.base import ModelSerializer
from django_serializer.serializer.fields import SerializerField

from vkrb.activity.serializers import ActivitySiItemSerializer, ActivityGiItemSerializer
from vkrb.attachment.serializers import AttachmentSerializer
from vkrb.core.serializers import UserSerializer
from vkrb.expert.serializers import ExpertSerializer
from vkrb.favorites.models import FavoriteItem
from vkrb.recourse.models import Recourse, Specialty, RecourseLike


class RecourseSerializer(ModelSerializer):
    children = SerializerField(source='get_childs')
    likes = SerializerField(source='get_likes')
    user = SerializerField(source='get_owner')
    photo = SerializerField(source='get_recourse_photo')
    is_liked = SerializerField(source='get_recourse_liked')
    expert = SerializerField(source='get_expert')
    is_fav = SerializerField(source='get_fav')
    specialty = SerializerField(source='get_spec')
    si = SerializerField(source='get_si')
    gi = SerializerField(source='get_gi')

    class Meta:
        model = Recourse
        exclude = ('si_id', 'gi_id')

    def __init__(self, *args, **kwargs):
        self.request_user = kwargs.pop('request_user')
        super().__init__(*args, **kwargs)

    def get_expert(self, obj):
        return ExpertSerializer(obj.expert, user=self.request_user).serialize()

    def get_recourse_photo(self, obj):
        return AttachmentSerializer(obj.photo).serialize()

    def get_spec(self, obj):
        return SpecialtySerializer(obj.specialty).serialize()

    def get_recourse_liked(self, obj):
        return RecourseLike.objects.filter(
            user_id=self.request_user.pk,
            recourse_id=obj.pk
        ).exists()

    def get_likes(self, obj):
        count = RecourseLike.objects.filter(recourse_id=obj.pk).count()
        return count

    def get_owner(self, obj):
        user = obj.user
        return UserSerializer(user).serialize()

    def get_childs(self, obj):
        if obj.parent is None:
            children = Recourse.objects.filter(parent=obj).annotate(
                num_likes=Count('recourselike')).order_by('-num_likes')
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

    def get_si(self, obj):
        return ActivitySiItemSerializer(obj.si, user=self.request_user).serialize()

    def get_gi(self, obj):
        return ActivityGiItemSerializer(obj.gi, user=self.request_user).serialize()


class SpecialtySerializer(ModelSerializer):
    icon = SerializerField(source='get_specialty_icon')

    class Meta:
        model = Specialty

    def get_specialty_icon(self, obj):
        return AttachmentSerializer(obj.icon).serialize()


class RecourseLikeSerializer(ModelSerializer):
    class Meta:
        model = RecourseLike
