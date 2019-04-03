from django.db import models

from vkrb.search import SearchModelMixin


class TextType:
    ABOUT_KNPK = 'about_knpk'

    CHOICES = (
        (ABOUT_KNPK, 'О КНПК'),
    )


class Text(SearchModelMixin, models.Model):
    type = models.CharField(
        max_length=255, unique=True,
        choices=TextType.CHOICES,
        verbose_name='Тип текста'
    )
    content = models.TextField(verbose_name='Текст')

    class Meta:
        verbose_name = 'Текст'
        verbose_name_plural = 'Текста'

    def __str__(self):
        return f'{self.get_type_display()}'

    def get_text_for_search_vector(self):
        return self.content
