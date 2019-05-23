from django.db import models
from django.utils import timezone
from django.utils.safestring import mark_safe

from vkrb.attachment.models import Attachment
from vkrb.core.utils import build_url
from vkrb.search import SearchModelMixin


class AttachemntInNewsItem(models.Model):
    class Meta:
        db_table = "attachment_newsitem"
        verbose_name = 'Фото'
        verbose_name_plural = 'Фото'
        ordering = ('order',)

    newsitem = models.ForeignKey('newsitem.NewsItem',
                                 verbose_name="Новость",
                                 on_delete=models.CASCADE)
    attachment = models.ForeignKey('attachment.Attachment',
                                   verbose_name="Фото",
                                   related_name='attachments',
                                   on_delete=models.CASCADE)
    main = models.BooleanField(default=False,
                               verbose_name='Главное фото',
                               help_text="Рекомендуемое соотношение сторон для главного фото 4:4")
    order = models.PositiveIntegerField(default=0, blank=False, null=False)

    def __str__(self):
        return self.attachment.file.url


class CategoryNewsItem(models.Model):
    class Meta:
        verbose_name = 'категория новости'
        verbose_name_plural = 'категории новостей'
        ordering = ('order',)

    title = models.CharField(max_length=255, verbose_name='Название категории')
    order = models.PositiveIntegerField(default=0, blank=False, null=False)

    def __str__(self):
        return self.title


class NewsKeyword(models.Model):
    class Meta:
        verbose_name = 'Ключевое слово'
        verbose_name_plural = 'Ключевые слова'

    title = models.CharField(max_length=255, verbose_name='Название')

    def __str__(self):
        return self.title


class NewsItem(SearchModelMixin, models.Model):
    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

    title = models.CharField(max_length=255, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст')
    attachments = models.ManyToManyField(Attachment,
                                         through=AttachemntInNewsItem,
                                         verbose_name='Фото')
    # category = models.ForeignKey(CategoryNewsItem,
    #                              null=True,
    #                              default=None,
    #                              blank=True,
    #                              verbose_name='Категория',
    #                              on_delete=models.SET_NULL)
    created = models.DateTimeField(default=timezone.now,
                                   verbose_name='Дата публикации новости')

    # keywords = models.TextField(verbose_name='Ключевые слова', null=True, blank=True, help_text='Через пробел')
    keywords = models.ManyToManyField(NewsKeyword, verbose_name='Ключевые слова', null=True, blank=True,
                                      )

    def __str__(self):
        return self.title

    def image_tag(self):
        try:
            main_photo = self.attachments.get(attachments__main=True)
            return mark_safe(
                '<div style="background-position: center;'
                ' background-repeat: no-repeat;'
                ' background-size: cover;'
                ' background-image: url(%s);'
                ' height: 150px;'
                ' width: 150px;" />' % build_url(main_photo.file.url))
        except Attachment.DoesNotExist:
            return '-'

    image_tag.short_description = 'Главное фото'
    image_tag.allow_tags = True

    def get_text_for_search_vector(self):
        return ' '.join(filter(lambda v: bool(v), [
            self.title, self.text, self.keywords.all()
        ]))
