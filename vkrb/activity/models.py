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
                               verbose_name='Аббревиатура факультета')
    description = models.TextField(null=True, blank=True,
                                   verbose_name='Описание')
    link = models.URLField(null=True, max_length=1000, verbose_name='Ссылка')
    lat = models.FloatField(null=True, verbose_name='Широта', blank=True)
    lng = models.FloatField(null=True, verbose_name='Долгота', blank=True)
    specialty = models.CharField(max_length=255, null=True, blank=True,
                                 verbose_name='Специализация')
    ceo = models.CharField(max_length=255, null=True, blank=True,
                           verbose_name='Декан факультета')

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
        verbose_name = 'Факультет'
        verbose_name_plural = 'Факультеты'

    def __str__(self):
        return self.title

    def get_text_for_search_vector(self):
        return ' '.join(filter(lambda v: bool(v), [
            self.title, self.description
        ]))


class SiItem(SearchModelMixin, models.Model):
    gi = models.ForeignKey(GiItem, on_delete=models.CASCADE, verbose_name='Факультет')
    photo = models.ForeignKey(Attachment, on_delete=models.CASCADE,
                              blank=True,
                              null=True,
                              verbose_name='Фото')
    title = models.CharField(max_length=255,
                             verbose_name='Заголовок')
    acronym = models.CharField(max_length=255, null=True,
                               verbose_name='Аббревиатура кафедры')
    description = models.TextField(null=True, blank=True,
                                   verbose_name='Описание')
    link = models.URLField(max_length=1000,
                           verbose_name='Ссылка')
    lat = models.FloatField(verbose_name='Широта', blank=True, null=True)
    lng = models.FloatField(verbose_name='Долгота', blank=True, null=True)
    specialty = models.CharField(max_length=255, null=True, blank=True,
                                 verbose_name='Специализация')
    ceo = models.CharField(max_length=255, null=True, blank=True,
                           verbose_name='заведующий кафедрой')
    contact_info = models.TextField(null=True, blank=True,
                                    verbose_name='Контактная информация')
    activity_course = models.TextField(null=True, blank=True,
                                       verbose_name='Ключевые направления деятельности')
    history = models.TextField(null=True, blank=True,
                               verbose_name='Историческая справка')
    pdf = models.ForeignKey(Attachment, null=True, blank=True, verbose_name=u'PDF',
                            on_delete=models.SET_NULL, related_name='si_pdf')

    class Meta:
        verbose_name = 'кафедра'
        verbose_name_plural = 'кафедры'

    def __str__(self):
        return self.title

    def get_text_for_search_vector(self):
        return ' '.join(filter(lambda v: bool(v), [
            self.title, self.description
        ]))
