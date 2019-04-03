from django.contrib.contenttypes.models import ContentType
from django_serializer.serializer.base import ModelSerializer
from django_serializer.serializer.fields import SerializerField

from vkrb.attachment.serializers import AttachmentSerializer
from vkrb.education.models import (
    CategoryInternalEducation,
    InternalEducation,
    CategoryLibrary,
    CategoryCatalog,
    CatalogItem,
    Reduction,
    ScienceArticle, Literature)
from vkrb.favorites.models import FavoriteItem


class CategoryInternalEducationSerializer(ModelSerializer):
    class Meta:
        model = CategoryInternalEducation


class CategoryLibrarySerializer(ModelSerializer):
    photo = SerializerField(source='get_image')

    class Meta:
        model = CategoryLibrary
        exclude = ('photo_id',)

    def get_image(self, obj):
        return AttachmentSerializer(obj.photo).serialize()


class CategoryCatalogSerializer(ModelSerializer):
    photo = SerializerField(source='get_image')
    library = SerializerField(source='get_library')

    class Meta:
        model = CategoryCatalog
        exclude = ('photo_id',)

    def get_image(self, obj):
        return AttachmentSerializer(obj.photo).serialize()

    def get_library(self, obj):
        return CategoryLibrarySerializer(obj.library).serialize()


class InternalEducationSerializer(ModelSerializer):
    photo = SerializerField(source='get_image')
    pdf = SerializerField(source='get_pdf')
    type = SerializerField(source='get_type')
    is_fav = SerializerField(source='get_fav')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    class Meta:
        model = InternalEducation
        exclude = ('photo_id', 'pdf_id', 'type_id')

    def get_image(self, obj):
        return AttachmentSerializer(obj.photo).serialize()

    def get_type(self, obj):
        return CategoryInternalEducationSerializer(obj.type).serialize()

    def get_pdf(self, obj):
        return AttachmentSerializer(obj.pdf).serialize()

    def get_fav(self, obj):
        content_type = ContentType.objects.get(model='internaleducation')
        is_fav = FavoriteItem.objects.filter(user=self.user,
                                             content_type=content_type,
                                             object_id=obj.id).exists()
        return is_fav


class CatalogItemSerializer(ModelSerializer):
    photo = SerializerField(source='get_image')
    is_fav = SerializerField(source='get_fav')
    type = SerializerField(source='get_type')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    class Meta:
        model = CatalogItem
        exclude = ('photo_id', 'order')

    def get_image(self, obj):
        return AttachmentSerializer(obj.photo).serialize()

    def get_fav(self, obj):
        content_type = ContentType.objects.get(model='catalogitem')
        is_fav = FavoriteItem.objects.filter(user=self.user,
                                             content_type=content_type,
                                             object_id=obj.id).exists()
        return is_fav

    def get_type(self, obj):
        return CategoryCatalogSerializer(obj.type).serialize()


class ShortCatalogItemSerializer(ModelSerializer):
    photo = SerializerField(source='get_image')
    is_fav = SerializerField(source='get_fav')
    type = SerializerField(source='get_type')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    class Meta:
        model = CatalogItem
        exclude = (
            'photo_id', 'order', "mode", "target",
            "advantages", "disadvantages",
            "application", "effect", "example",
            "result", "not_applied", "reasons",
            "analogs", "literature")

    def get_image(self, obj):
        return AttachmentSerializer(obj.photo).serialize()

    def get_fav(self, obj):
        content_type = ContentType.objects.get(model='catalogitem')
        is_fav = FavoriteItem.objects.filter(user=self.user,
                                             content_type=content_type,
                                             object_id=obj.id).exists()
        return is_fav

    def get_type(self, obj):
        return CategoryCatalogSerializer(obj.type).serialize()


class ReductionSerializer(ModelSerializer):
    class Meta:
        model = Reduction
        exclude = ('order',)


class ShortScienceArticleSerializer(ModelSerializer):
    photo = SerializerField(source='get_photo')
    is_fav = SerializerField(source='get_fav')
    library = SerializerField(source='get_library')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    class Meta:
        model = ScienceArticle
        fields = ('id', 'library_id', 'title', 'date_of_issued', 'author', 'keywords')

    def get_photo(self, obj):
        return AttachmentSerializer(obj.photo).serialize()

    def get_fav(self, obj):
        content_type = ContentType.objects.get(model='sciencearticle')
        if self.user.is_anonymous:
            return False
        is_fav = FavoriteItem.objects.filter(user=self.user,
                                             content_type=content_type,
                                             object_id=obj.id).exists()
        return is_fav

    def get_library(self, obj):
        return CategoryLibrarySerializer(obj.library).serialize()


class ScienceArticleSerializer(ModelSerializer):
    photo = SerializerField(source='get_photo')
    attachment = SerializerField(source='get_attachment')
    is_fav = SerializerField(source='get_fav')
    library = SerializerField(source='get_library')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    class Meta:
        model = ScienceArticle
        exclude = ('attachment_id', 'photo_id')

    def get_photo(self, obj):
        return AttachmentSerializer(obj.photo).serialize()

    def get_attachment(self, obj):
        return AttachmentSerializer(obj.attachment).serialize()

    def get_fav(self, obj):
        content_type = ContentType.objects.get(model='sciencearticle')
        if self.user.is_anonymous:
            return False
        is_fav = FavoriteItem.objects.filter(user=self.user,
                                             content_type=content_type,
                                             object_id=obj.id).exists()
        return is_fav

    def get_library(self, obj):
        return CategoryLibrarySerializer(obj.library).serialize()


class LiteratureSerializer(ModelSerializer):
    photo = SerializerField(source='get_photo')
    is_fav = SerializerField(source='get_fav')
    library = SerializerField(source='get_library')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    class Meta:
        model = Literature
        exclude = ('photo_id',)

    def get_photo(self, obj):
        return AttachmentSerializer(obj.photo).serialize()

    def get_fav(self, obj):
        content_type = ContentType.objects.get(model='literature')
        if self.user.is_anonymous:
            return False
        is_fav = FavoriteItem.objects.filter(user=self.user,
                                             content_type=content_type,
                                             object_id=obj.id).exists()
        return is_fav

    def get_library(self, obj):
        return CategoryLibrarySerializer(obj.library).serialize()
