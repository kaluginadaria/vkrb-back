from django.contrib.contenttypes.models import ContentType
from django_serializer.serializer.base import ModelSerializer
from django_serializer.serializer.fields import SerializerField

from vkrb.attachment.serializers import AttachmentSerializer
from vkrb.digest.models import DigestCategory, Digest, Article
from vkrb.favorites.models import FavoriteItem


class DigestCategorySerializer(ModelSerializer):
    class Meta:
        model = DigestCategory


class DigestSerializer(ModelSerializer):
    is_fav = SerializerField(source='get_fav')
    category = SerializerField(source='get_cat')
    icon = SerializerField(source='get_digest_icon')
    pdf = SerializerField(source='get_digest_pdf')

    class Meta:
        model = Digest
        exclude = ('icon_id', 'pdf_id')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def get_digest_icon(self, obj):
        return AttachmentSerializer(obj.icon).serialize()

    def get_digest_pdf(self, obj):
        return AttachmentSerializer(obj.pdf).serialize()

    def get_cat(self, obj):
        return DigestCategorySerializer(obj.category).serialize()

    def get_fav(self, obj):
        content_type = ContentType.objects.get(model='digest')
        is_fav = FavoriteItem.objects.filter(user=self.user,
                                             content_type=content_type,
                                             object_id=obj.id).exists()
        return is_fav


class ShortArticleSerializer(ModelSerializer):
    body = SerializerField(source='get_body')
    photo = SerializerField(source='get_photo')
    is_fav = SerializerField(source='get_fav')
    digest = SerializerField(source='get_dig')

    class Meta:
        model = Article
        exclude = ('body',)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def get_dig(self, obj):
        return DigestSerializer(obj.digest, user=self.user).serialize()

    def get_body(self, obj):
        return f'{obj.body[:200]}...' if len(obj.body) > 200 else obj.body

    def get_photo(self, obj):
        article_attachment = obj.article_attachments.all() \
            .order_by('order').first()

        return AttachmentSerializer(
            article_attachment.attachment if article_attachment else None
        ).serialize()

    def get_fav(self, obj):
        content_type = ContentType.objects.get(model='article')
        is_fav = FavoriteItem.objects.filter(user=self.user,
                                             content_type=content_type,
                                             object_id=obj.id).exists()
        return is_fav


class ArticleSerializer(ModelSerializer):
    photos = SerializerField(source='get_photos')
    is_fav = SerializerField(source='get_fav')
    digest = SerializerField(source='get_dig')

    class Meta:
        model = Article

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def get_dig(self, obj):
        return DigestSerializer(obj.digest, user=self.user).serialize()

    def get_photos(self, obj):
        attachments = obj.attachments.all()
        return AttachmentSerializer(attachments, multiple=True).serialize()

    def get_fav(self, obj):
        content_type = ContentType.objects.get(model='article')
        is_fav = FavoriteItem.objects.filter(user=self.user,
                                             content_type=content_type,
                                             object_id=obj.id).exists()
        return is_fav
