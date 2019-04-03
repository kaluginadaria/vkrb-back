from django.db import models
from django.utils.safestring import mark_safe

from vkrb.attachment.models import Attachment
from vkrb.core.utils import build_url
from vkrb.search import SearchModelMixin


class Formula(SearchModelMixin, models.Model):
    class Meta:
        verbose_name = 'Формула'
        verbose_name_plural = 'Формулы'
        ordering = ('order',)

    title = models.CharField(max_length=255, verbose_name='Название')
    key = models.CharField(max_length=255, verbose_name='Ключ')
    photo = models.ForeignKey(Attachment, on_delete=models.CASCADE,
                              verbose_name='Картинка формулы')
    order = models.PositiveIntegerField(default=0, blank=False, null=False)

    keywords = models.TextField(verbose_name='Ключевые слова', null=True, blank=True, help_text='Через пробел')

    def __str__(self):
        return f'{self.title}'

    def image_tag(self):
        try:
            return mark_safe(
                '<div style="background-position: center;'
                ' background-repeat: no-repeat;'
                ' background-size: cover;'
                ' background-image: url(%s);'
                ' height: 150px;'
                ' width: 150px;" />' % build_url(self.photo.file.url))
        except Attachment.DoesNotExist:
            return '-'

    image_tag.short_description = 'Формула'
    image_tag.allow_tags = True

    def get_text_for_search_vector(self):
        return ' '.join(filter(lambda v: bool(v), [
            self.title, self.keywords
        ]))
