from django_serializer.serializer.base import ModelSerializer

from vkrb.activity.serializers import ActivityGiItemSerializer, ActivitySiItemSerializer
from vkrb.calc.serializers import FormulaSerializer
from vkrb.digest.serializers import DigestSerializer, ShortArticleSerializer
from vkrb.education.serializers import (
    InternalEducationSerializer,
    ShortScienceArticleSerializer,
    LiteratureSerializer,
    CatalogItemSerializer
)
from vkrb.expert.serializers import ExpertSerializer
from vkrb.favorites.models import (
    FavoriteItem)
from vkrb.newsitem.serializers import NewsItemSerializer
from vkrb.recourse.serializers import RecourseSerializer


class FavoriteSerializer(ModelSerializer):
    SERIALIZERS = {
        'digest.digest': DigestSerializer,
        'activity.siitem': ActivitySiItemSerializer,
        'activity.giitem': ActivityGiItemSerializer,
        'digest.article': ShortArticleSerializer,
        'newsitem.newsitem': NewsItemSerializer,
        'recourse.recourse': RecourseSerializer,
        'expert.expert': ExpertSerializer,
        'education.internaleducation': InternalEducationSerializer,
        'education.sciencearticle': ShortScienceArticleSerializer,
        'education.literature': LiteratureSerializer,
        'calc.formula': FormulaSerializer,
        'education.catalogitem': CatalogItemSerializer
    }

    class Meta:
        model = FavoriteItem
        exclude = ('id', 'content_type_id', 'object_id')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def serialize(self):
        if self.obj is None:
            return None
        result = {}

        for obj_item in self.obj:
            entity_type = f'{obj_item.content_type.app_label}.' \
                          f'{obj_item.content_type.model}'
            serializer_class = self.SERIALIZERS[entity_type]
            kwargs = {}
            if issubclass(serializer_class, (RecourseSerializer,)):
                kwargs['request_user'] = self.user
            else:
                kwargs['user'] = self.user

            result.setdefault(entity_type, [])
            if obj_item.content_object:
                result[entity_type].append(
                    serializer_class(obj_item.content_object, **kwargs).serialize()
                )

        return result


class FavoriteItemSerializer(ModelSerializer):
    class Meta:
        model = FavoriteItem
