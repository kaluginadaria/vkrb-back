from colorfield.fields import ColorField
from django.db import models

from vkrb.attachment.models import Attachment
from vkrb.search import SearchModelMixin


class EventType(models.Model):
    class Meta:
        verbose_name = 'Тип события'
        verbose_name_plural = 'Типы событий'

    name = models.CharField(max_length=255, verbose_name='Название')
    color = ColorField(default='#FF0000', verbose_name='Цвет рамки в календаре')

    def __str__(self):
        return self.name


class Event(SearchModelMixin, models.Model):
    class Meta:
        verbose_name = 'Событие'
        verbose_name_plural = 'События'

    subject = models.TextField(verbose_name='Тема')
    type = models.ForeignKey(EventType, on_delete=models.SET_NULL, null=True,
                             verbose_name='Тип события')
    start = models.DateTimeField(
        verbose_name='Старт события',
        help_text='Если событие одним днем, заполните только старт.'
    )
    end = models.DateTimeField(null=True, blank=True,
                               verbose_name='Конец события')
    location = models.CharField(max_length=255, verbose_name='Место')

    pdf = models.ForeignKey(Attachment, null=True, on_delete=models.CASCADE,
                            verbose_name='Загрузка PDF файла')

    def __str__(self):
        return self.subject

    def get_text_for_search_vector(self):
        return ' '.join([
            self.subject, self.location
        ])
