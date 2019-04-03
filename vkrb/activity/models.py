from django.db import models

from vkrb.attachment.models import Attachment
from vkrb.search import SearchModelMixin


class GiItem(SearchModelMixin, models.Model):
    photo = models.ForeignKey(Attachment, on_delete=models.CASCADE,
                              blank=True,
                              null=True,
                              verbose_name='Фото')
    title = models.CharField(max_length=255,
                             verbose_name='Заголовок')
    acronym = models.CharField(max_length=255, null=True,
                               verbose_name='Аббревиатура ГИ')
    description = models.TextField(null=True, blank=True,
                                   verbose_name='Описание')
    link = models.URLField(null=True,max_length=1000, verbose_name='Ссылка')
    lat = models.FloatField(null=True,verbose_name='Широта')
    lng = models.FloatField(null=True,verbose_name='Долгота')
    specialty = models.CharField(max_length=255, null=True, blank=True,
                                 verbose_name='Специализация')
    ceo = models.CharField(max_length=255, null=True, blank=True,
                           verbose_name='Генеральный директор')

    activity_course = models.TextField(null=True, blank=True,
                                       verbose_name='Ключевые направления деятельности')
    history = models.TextField(null=True, blank=True,
                               verbose_name='Историческая справка')
    contact_info = models.TextField(null=True, blank=True,
                                    verbose_name='Контактная информация')
    pdf = models.ForeignKey(Attachment, null=True, verbose_name=u'PDF',
                            on_delete=models.SET_NULL, related_name='gi_pdf'
                            )
    is_actual = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'ГИ'
        verbose_name_plural = 'ГИ'

    def __str__(self):
        return self.title

    def get_text_for_search_vector(self):
        return ' '.join(filter(lambda v: bool(v), [
            self.title, self.description
        ]))


class SiItem(SearchModelMixin, models.Model):
    gi = models.ForeignKey(GiItem, blank=True, on_delete=models.CASCADE, verbose_name='ГИ')
    photo = models.ForeignKey(Attachment, on_delete=models.CASCADE,
                              blank=True,
                              null=True,
                              verbose_name='Фото')
    title = models.CharField(max_length=255,
                             verbose_name='Заголовок')
    acronym = models.CharField(max_length=255, null=True,
                               verbose_name='Аббревиатура СИ')
    description = models.TextField(null=True, blank=True,
                                   verbose_name='Описание')
    link = models.URLField(max_length=1000,
                           verbose_name='Ссылка')
    lat = models.FloatField(verbose_name='Широта')
    lng = models.FloatField(verbose_name='Долгота')
    specialty = models.CharField(max_length=255, null=True, blank=True,
                                 verbose_name='Специализация')
    ceo = models.CharField(max_length=255, null=True, blank=True,
                           verbose_name='Генеральный директор')
    contact_info = models.TextField(null=True, blank=True,
                                    verbose_name='Контактная информация')
    activity_course = models.TextField(null=True, blank=True,
                                       verbose_name='Ключевые направления деятельности')
    history = models.TextField(null=True, blank=True,
                               verbose_name='Историческая справка')
    pdf = models.ForeignKey(Attachment, null=True, verbose_name=u'PDF',
                            on_delete=models.SET_NULL, related_name='si_pdf')

    class Meta:
        verbose_name = 'СИ'
        verbose_name_plural = 'СИ'

    def __str__(self):
        return self.title

    def get_text_for_search_vector(self):
        return ' '.join(filter(lambda v: bool(v), [
            self.title, self.description
        ]))
