from django.db import models
from django.utils.safestring import mark_safe

from vkrb.attachment.models import Attachment
from vkrb.core.utils import build_url
from vkrb.search import SearchModelMixin


class DigestCategory(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    order = models.PositiveIntegerField(default=0, blank=False, null=False,
                                        verbose_name='Порядок')

    class Meta:
        verbose_name = 'Категория дайджеста'
        verbose_name_plural = 'Категории дайджестов'
        ordering = ('order',)

    def __str__(self):
        return self.title


class Digest(SearchModelMixin, models.Model):
    category = models.ForeignKey(DigestCategory, on_delete=models.CASCADE,
                                 verbose_name='Категория')
    icon = models.ForeignKey(Attachment, null=True, verbose_name=u'Фото дайджеста', on_delete=models.SET_NULL,
                             related_name='icon')
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    order = models.PositiveIntegerField(default=0, blank=False, null=False,
                                        verbose_name='Порядок')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')
    pdf = models.ForeignKey(Attachment, null=True, verbose_name=u'PDF', on_delete=models.SET_NULL)

    class Meta:
        verbose_name = 'Дайджест'
        verbose_name_plural = 'Дайджесты'
        ordering = ('order',)

    def __str__(self):
        return self.title

    def get_text_for_search_vector(self):
        return self.title


class Article(SearchModelMixin, models.Model):
    attachments = models.ManyToManyField(
        Attachment, through='digest.ArticleAttachment',
        verbose_name='Прикрепления'
    )
    digest = models.ForeignKey(Digest, on_delete=models.CASCADE,
                               verbose_name='Дайджест')
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    body = models.TextField(verbose_name='Текст статьи')
    keywords = models.TextField(verbose_name='Ключевые слова', null=True, blank=True, help_text='Через пробел')

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def __str__(self):
        return self.title

    def get_text_for_search_vector(self):
        return ' '.join(filter(lambda v: bool(v), [
            self.title, self.body, self.keywords
        ]))


class ArticleAttachment(models.Model):
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE,
        verbose_name='Статья', related_name='article_attachments'
    )
    attachment = models.ForeignKey(Attachment, on_delete=models.CASCADE,
                                   verbose_name='Прикрепление')
    order = models.PositiveIntegerField(default=0, blank=False, null=False)

    class Meta:
        verbose_name = 'Прикрепление'
        verbose_name_plural = 'Прикрепления'
        ordering = ('order',)

    def __str__(self):
        return f'Прикрепление {self.id}'

    def image_tag(self):
        main_photo = self.attachment
        if not main_photo:
            return '-'
        try:
            return mark_safe(
                '<div style="background-position: center;'
                ' background-repeat: no-repeat;'
                ' background-size: cover;'
                ' background-image: url(%s);'
                ' height: 150px;'
                ' width: 150px;" />' % build_url(main_photo.file.url))
        except Attachment.DoesNotExist:
            return '-'

    image_tag.short_description = 'Фото'
    image_tag.allow_tags = True
