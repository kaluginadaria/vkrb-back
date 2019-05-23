from django.db import models
from django.utils.safestring import mark_safe

from vkrb.attachment.models import Attachment
from vkrb.core.utils import build_url
from vkrb.search import SearchModelMixin


class CategoryInternalEducation(models.Model):
    class Meta:
        verbose_name = 'категория внутреннего обучения'
        verbose_name_plural = 'категории внутреннего обучения'
        ordering = ('order',)

    title = models.CharField(max_length=255, verbose_name='Название категории')
    order = models.PositiveIntegerField(default=0, blank=False, null=False,
                                        verbose_name='Порядок')

    def __str__(self):
        return self.title


class InternalEducation(models.Model):
    class Meta:
        verbose_name = 'Внутреннее обучения'
        verbose_name_plural = 'Внутренние обучения'

    title = models.CharField(max_length=255, verbose_name='Заголовок')
    type = models.ForeignKey(CategoryInternalEducation,
                             on_delete=models.CASCADE, verbose_name='Категория')
    location = models.CharField(max_length=255, verbose_name='Место')
    photo = models.ForeignKey(Attachment, on_delete=models.CASCADE,
                              related_name='photo',
                              verbose_name='Картинка обучения')
    pdf = models.ForeignKey(Attachment, on_delete=models.CASCADE,
                            related_name='pdf',
                            verbose_name='PDF обучения')

    keywords = models.TextField(verbose_name='Ключевые слова',
                                null=True, blank=True,
                                help_text='Через пробел')

    def __str__(self):
        return self.title

    def image_tag(self):
        try:
            main_photo = self.photo
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

    def get_text_for_search_vector(self):
        return ' '.join(filter(lambda v: bool(v), [
            self.title, self.keywords
        ]))


class CategoryLibrary(models.Model):
    class Meta:
        verbose_name = 'категория библиотеки'
        verbose_name_plural = 'категории библиотеки'
        ordering = ('order',)

    title = models.CharField(max_length=255, verbose_name='Название категории')
    photo = models.ForeignKey(Attachment, on_delete=models.CASCADE,
                              related_name='category_library_photo',
                              verbose_name='Иконка категории')
    order = models.PositiveIntegerField(default=0, blank=False, null=False,
                                        verbose_name='Порядок')

    def __str__(self):
        return self.title


class CategoryCatalog(models.Model):
    class Meta:
        verbose_name = 'категория справочника'
        verbose_name_plural = 'категории справочника'
        ordering = ('order',)

    title = models.CharField(max_length=255, verbose_name='Название категории')
    library = models.ForeignKey(CategoryLibrary, on_delete=models.CASCADE,
                                verbose_name='Категория библиотеки')
    photo = models.ForeignKey(Attachment, on_delete=models.CASCADE,
                              related_name='category_catalog_photo',
                              verbose_name='Иконка категории')
    order = models.PositiveIntegerField(default=0, blank=False, null=False,
                                        verbose_name='Порядок')

    def __str__(self):
        return self.title


class CatalogItem(SearchModelMixin, models.Model):
    class Meta:
        verbose_name = 'Запись в справочнике'
        verbose_name_plural = 'Записи в справочнике'
        ordering = ('order',)

    title = models.CharField(max_length=255, verbose_name='Заголовок')
    type = models.ForeignKey(CategoryCatalog, on_delete=models.CASCADE,
                             verbose_name='Категория')
    photo = models.ForeignKey(Attachment, on_delete=models.CASCADE,
                              related_name='catalog_photo',
                              verbose_name='Графическое изображение')
    description = models.TextField(null=True, blank=True,
                                   verbose_name='Описание технологии')
    mode = models.TextField(null=True, blank=True,
                            verbose_name='Проблематика/специфика применения')
    target = models.TextField(null=True, blank=True,
                              verbose_name='Цель технологии')
    advantages = models.TextField(null=True, blank=True,
                                  verbose_name='Преимущества технологии')
    disadvantages = models.TextField(null=True, blank=True,
                                     verbose_name='Недостатки')
    application = models.TextField(null=True, blank=True,
                                   verbose_name='Применение')
    effect = models.TextField(null=True, blank=True,
                              verbose_name='Потенциальный эффект')
    example = models.TextField(null=True, blank=True,
                               verbose_name='Пример применения технологии')
    result = models.TextField(null=True, blank=True,
                              verbose_name='Результат применения')
    not_applied = models.TextField(null=True, blank=True,
                                   verbose_name='Пример, где технология не получила применения')
    reasons = models.TextField(null=True, blank=True,
                               verbose_name='Причины отказа от технологии')
    analogs = models.TextField(null=True, blank=True,
                               verbose_name='Российские и зарубежные аналоги технологи')
    literature = models.TextField(null=True, blank=True,
                                  verbose_name='Литература')
    order = models.PositiveIntegerField(default=0, blank=False, null=False,
                                        verbose_name='Порядок')
    keywords = models.TextField(verbose_name='Ключевые слова', null=True,
                                blank=True, help_text='Через пробел')

    def __str__(self):
        return self.title

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

    image_tag.short_description = 'Фото'
    image_tag.allow_tags = True

    def get_text_for_search_vector(self):
        return ' '.join(filter(lambda v: bool(v), [
            self.title, self.description, self.target, self.advantages,
            self.analogs, self.keywords
        ]))


class Reduction(models.Model):
    class Meta:
        verbose_name = 'сокращение и обозначение'
        verbose_name_plural = 'сокращения и обозначения'
        ordering = ('order',)

    reduction = models.CharField(max_length=255, verbose_name='Сокращение')
    transcript = models.TextField(verbose_name='Расшифровка')
    library = models.ForeignKey(CategoryLibrary, on_delete=models.CASCADE,
                                verbose_name='Категория библиотеки')
    order = models.PositiveIntegerField(default=0, blank=False, null=False,
                                        verbose_name='Порядок')

    def __str__(self):
        return self.reduction


class ScienceArticle(SearchModelMixin, models.Model):
    library = models.ForeignKey(CategoryLibrary, on_delete=models.CASCADE,
                                verbose_name='Категория',
                                null=True, blank=True)
    photo = models.ForeignKey(
        Attachment, on_delete=models.CASCADE,
        verbose_name='Изображение', related_name='photo_articles'
    )
    attachment = models.ForeignKey(
        Attachment, on_delete=models.CASCADE,
        verbose_name='Приложение', default=None, related_name='attachment_articles',

    )
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    date_of_issued = models.IntegerField(
        verbose_name='Год издания',
        blank=True,
        null=True, default=None
    )
    author = models.TextField(verbose_name='Автор', blank=True, null=True,
                              default=None)
    keywords = models.TextField(verbose_name='Ключевые слова', null=True,
                                blank=True, help_text='Через пробел')

    problems = models.TextField(verbose_name='Проблематика', blank=True,
                                null=True, default=None)
    decision = models.TextField(verbose_name='Решение', blank=True,
                                null=True, default=None)
    result = models.TextField(verbose_name='Результат', blank=True, null=True,
                              default=None)
    body = models.TextField(verbose_name='Текст статьи', blank=True, null=True,
                            default=None)

    class Meta:
        verbose_name = 'Научная статья'
        verbose_name_plural = 'Научные статьи'

    def __str__(self):
        return self.title

    def image_tag(self):
        main_photo = self.photo
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

    def get_text_for_search_vector(self):
        return ' '.join(filter(lambda v: bool(v), [
            self.title, self.author, self.keywords,
            self.problems, self.decision, self.result, self.body
        ]))


class Literature(SearchModelMixin, models.Model):
    library = models.ForeignKey(CategoryLibrary, on_delete=models.CASCADE,
                                verbose_name='Категория',
                                null=True, blank=True)
    photo = models.ForeignKey(
        Attachment, on_delete=models.CASCADE,
        verbose_name='Изображение'
    )

    title = models.CharField(max_length=255, verbose_name='Заголовок')
    date_of_issued = models.IntegerField(
        verbose_name='Год издания',
        blank=True,
        null=True, default=None
    )
    author = models.TextField(verbose_name='Авторы', blank=True, null=True,
                              default=None)
    keywords = models.TextField(verbose_name='Ключевые слова', null=True,
                                blank=True, help_text='Через пробел')

    class Meta:
        verbose_name = 'Литература'
        verbose_name_plural = 'Литература'

    def __str__(self):
        return self.title

    def image_tag(self):
        main_photo = self.photo
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

    def get_text_for_search_vector(self):
        return ' '.join(filter(lambda v: bool(v), [
            self.title, self.author, self.keywords
        ]))
