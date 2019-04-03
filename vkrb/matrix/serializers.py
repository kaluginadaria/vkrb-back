from django_serializer.serializer.base import ModelSerializer
from django_serializer.serializer.fields import SerializerField

from vkrb.attachment.serializers import AttachmentSerializer
from vkrb.matrix.models import MatrixItem


class MatrixSerializer(ModelSerializer):
    children = SerializerField(source='get_childs')
    title = SerializerField(source='get_title')
    photo = SerializerField(source='get_photo')
    text = SerializerField(source='get_text')

    class Meta:
        model = MatrixItem
        exclude = ('photo_id', 'parent',
                   'parent_id', 'lft',
                   'level', 'rght', 'tree_id')

    def get_photo(self, obj):
        return AttachmentSerializer(obj.photo).serialize()

    def get_text(self, obj):
        return obj.text

    def get_title(self, obj):
        return obj.title

    def get_childs(self, obj):
        children = obj.get_children()
        return MatrixSerializer(
            children,
            multiple=True,

        ).serialize()


class MatrixItemSerializer(ModelSerializer):
    title = SerializerField(source='get_title')
    photo = SerializerField(source='get_photo')
    text = SerializerField(source='get_text')

    class Meta:
        model = MatrixItem
        exclude = ('photo_id', 'parent',
                   'parent_id', 'lft',
                   'level', 'rght', 'tree_id')

    def get_photo(self, obj):
        return AttachmentSerializer(obj.photo).serialize()

    def get_text(self, obj):
        return obj.text

    def get_title(self, obj):
        return obj.title
