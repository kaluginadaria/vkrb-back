from django.contrib.contenttypes.models import ContentType
from django_serializer.serializer.base import ModelSerializer
from django_serializer.serializer.fields import SerializerField

from vkrb.attachment.serializers import AttachmentSerializer
from vkrb.favorites.models import FavoriteItem
from vkrb.newsitem.models import NewsItem, CategoryNewsItem


class NewsItemSerializer(ModelSerializer):
    photos = SerializerField(source='get_photos')
    main_photo = SerializerField(source='get_main_photo')
    is_fav = SerializerField(source='get_fav')
    category = SerializerField(source='get_category')
    keywords = SerializerField(source='get_keywords')


    class Meta:
        model = NewsItem
        exclude = ('keywords',)



    def get_keywords(self, obj):
        return obj.keywords.split(' ')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def get_main_photo(self, obj):
        main = obj.attachments \
            .filter(attachments__main=True) \
            .order_by('attachments__order') \
            .first()
        return AttachmentSerializer(main).serialize()

    def get_photos(self, obj):
        photos = obj.attachments.all().order_by('attachments__order')
        return AttachmentSerializer(photos, multiple=True).serialize()

    def get_fav(self, obj):
        content_type = ContentType.objects.get(model='newsitem')
        is_fav = FavoriteItem.objects.filter(user=self.user,
                                             content_type=content_type,
                                             object_id=obj.id).exists()
        return is_fav

    def get_category(self, obj):
        return CategoryNewsItemSerializer(obj.category).serialize()


class CategoryNewsItemSerializer(ModelSerializer):
    class Meta:
        model = CategoryNewsItem
