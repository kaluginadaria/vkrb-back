from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

from vkrb.attachment.models import Attachment
from vkrb.search import SearchModelMixin


class MatrixItem(SearchModelMixin, MPTTModel, models.Model):
    parent = TreeForeignKey('self', on_delete=models.CASCADE,
                            null=True, blank=True, related_name='children',
                            verbose_name='Название родительской компетенции')

    title = models.CharField(max_length=255, verbose_name='Название раздела')

    photo = models.ForeignKey(Attachment, null=True, blank=True,
                              verbose_name='Прикрепить фото к элементу матрицы',
                              on_delete=models.CASCADE)

    text = models.TextField(null=True, blank=True,
                            verbose_name='Текст раздела')

    class MPTTMeta:
        order_insertion_by = ['title']

    class Meta:
        verbose_name = 'Раздел матрицы компетенции'
        verbose_name_plural = 'Разделы матрицы компетенции'

    def __str__(self):
        return f'{self.title}'

    def get_text_for_search_vector(self):
        return ' '.join(filter(lambda v: bool(v), [
            self.title, self.text
        ]))
