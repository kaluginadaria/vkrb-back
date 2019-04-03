from django.db import models

from solo.models import SingletonModel


class SiteConfiguration(SingletonModel):

    block_changes = models.BooleanField(default=False, verbose_name='Запретить изменение всех профилей')

    def __unicode__(self):
        return u"Глобальные настройки"

    class Meta:
        verbose_name = "Глобальные настройки"
