from django.apps import apps
from django_serializer.serializer.base import ModelSerializer
from django_serializer.serializer.fields import SerializerField

from vkrb.activity.serializers import ActivityGiItemSerializer, ActivitySiItemSerializer
from vkrb.calc.serializers import FormulaSerializer
from vkrb.digest.serializers import DigestSerializer, ShortArticleSerializer, ArticleSerializer
from vkrb.education.serializers import (
    LiteratureSerializer,
    ScienceArticleSerializer,
    CatalogItemSerializer,
    InternalEducationSerializer)
from vkrb.event.serializers import EventSerializer
from vkrb.matrix.serializers import MatrixItemSerializer
from vkrb.newsitem.serializers import NewsItemSerializer
from vkrb.recourse.serializers import RecourseSerializer
from vkrb.search.models import SearchEntity
from vkrb.text.serializers import TextSerializer


class SearchEntitySerializer(ModelSerializer):
    SERIALIZERS = {
        'education.literature': LiteratureSerializer,
        'education.sciencearticle': ScienceArticleSerializer,
        'education.catalogitem': CatalogItemSerializer,
        'education.internaleducation': InternalEducationSerializer,
        'newsitem.newsitem': NewsItemSerializer,
        'digest.digest': DigestSerializer,
        'digest.article': ArticleSerializer,
        'text.text': TextSerializer,
        'recourse.recourse': RecourseSerializer,
        'event.event': EventSerializer,
        'calc.formula': FormulaSerializer,
        'matrix.matrixitem': MatrixItemSerializer,
        'activity.giitem': ActivityGiItemSerializer,
        'activity.siitem': ActivitySiItemSerializer
    }

    entity = SerializerField(source='get_entity')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    class Meta:
        model = SearchEntity
        exclude = ('search_vector', 'body', 'id')

    def get_serializer(self, entity_type, entity):
        kwargs = {}
        serializer_class = self.SERIALIZERS.get(entity_type)
        if serializer_class is None:
            raise ValueError(f'serializer for entity `{entity_type}` '
                             f'does not exist')

        if issubclass(serializer_class, (RecourseSerializer,)):
            kwargs['request_user'] = self.user
        elif not issubclass(serializer_class, (
                TextSerializer,
                EventSerializer,
                MatrixItemSerializer
        )):
            kwargs['user'] = self.user

        return serializer_class(entity, **kwargs)

    def get_entity(self, obj):
        entity = apps.get_model(
            obj.entity_type
        ).objects.filter(pk=obj.entity_id).first()
        serializer = self.get_serializer(obj.entity_type, entity)
        return serializer.serialize()

    def serialize(self):
        reformat_res = {}

        res = super().serialize()
        for item in res:
            entity_type = item['entity_type']
            entity = item['entity']

            if not entity:
                continue
            reformat_res.setdefault(entity_type, [])
            reformat_res[entity_type].append(entity)

        return reformat_res
