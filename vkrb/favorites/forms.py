from django import forms
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError

from vkrb.calc.models import Formula
from vkrb.digest.models import Digest, Article
from vkrb.education.models import InternalEducation, ScienceArticle, Literature, CatalogItem
from vkrb.expert.models import Expert
from vkrb.activity.models import GiItem,SiItem
from vkrb.favorites.models import FavoriteItem
from vkrb.newsitem.models import NewsItem
from vkrb.recourse.models import Recourse


class FavoriteForm(forms.ModelForm):
    ITEMS = {
        'digest': Digest,
        'giitem': GiItem,
        'siitem': SiItem,
        'article': Article,
        'newsitem': NewsItem,
        'recourse': Recourse,
        'expert': Expert,
        'internaleducation': InternalEducation,
        'sciencearticle': ScienceArticle,
        'literature': Literature,
        'formula': Formula,
        'catalogitem': CatalogItem
    }

    class Meta:
        model = FavoriteItem
        fields = ['object_id']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.model_name = kwargs.pop('content_type')
        self.content_type = ContentType.objects.get(model=self.model_name)
        super().__init__(*args, **kwargs)

    def clean_object_id(self):
        obj_id = self.cleaned_data.get('object_id')
        try:
            self.ITEMS[self.model_name].objects.get(id=obj_id)
            FavoriteItem.objects.get(user=self.user,
                                     content_type=self.content_type,
                                     object_id=obj_id)
            raise ValidationError('Пользователь уже добавил в избранное')
        except FavoriteItem.DoesNotExist:

            return obj_id
        except self.ITEMS[self.model_name].DoesNotExist:
            raise ValidationError('Данного объекта не существует')

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.user = self.user
        instance.content_type = self.content_type
        if commit:
            instance.save()

        return instance
