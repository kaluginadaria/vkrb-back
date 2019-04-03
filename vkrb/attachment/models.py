from django.core.exceptions import ValidationError
from django.db import models

from vkrb.application import settings
from vkrb.core.utils import build_url, build_file_url


def content_file_name(instance, filename):
    return '/'.join(['img', filename])


def validate_file_type(upload):
    type = upload.file.content_type
    if type not in settings.CONTENT_TYPE_FILES:
        raise ValidationError('Рекомендуемые форматы фото - .jpeg .png')


class Attachment(models.Model):
    file = models.FileField(verbose_name=u'Файл',
                            upload_to=content_file_name,
                            help_text="Форматы: .jpg .png .pdf",
                            validators=[validate_file_type])

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Прикрепление'
        verbose_name_plural = 'Прикрепления'

    def __str__(self):
        return f'Прикрепление #{self.pk}'

    def url(self):
        return build_url(self.file.url)

    def file_url(self):
        return build_file_url(self.file.name)
