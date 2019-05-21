from adminsortable2.admin import CustomInlineFormSet
from django import forms
from django.core.exceptions import ValidationError

from vkrb.newsitem.models import NewsItem


class NewsItemAttachmentAdminForm(CustomInlineFormSet):

    def clean(self):
        super().clean()
        photos = self.cleaned_data
        main_photos = [photo for photo in photos if photo['main'] is True]
        if len(main_photos) != 1:
            raise ValidationError('Выберете одно главное фото')


class NewsForm(forms.ModelForm):
    class Meta:
        model = NewsItem
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        keywords = cleaned_data.get('keywords')
        #todo: проверка на знаки ; . ,
        # if ['.', ',', ';'] in keywords:
        #     raise ValidationError({'keywords': 'Введите ключевые слова через пробел'})
        return cleaned_data
