from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from vkrb.core.models import User


class FavoriteItem(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id', )
    user = models.ForeignKey(User, verbose_name='Пользователь',
                             on_delete=models.CASCADE, default=None)

    class Meta:
        verbose_name = 'Раздел избранного'
        verbose_name_plural = 'Разделы избранного'
        unique_together = (('user', 'object_id', 'content_type'),)
