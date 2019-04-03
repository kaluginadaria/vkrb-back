from django.db import models
from smart_selects.db_fields import ChainedForeignKey

from vkrb.activity.models import SiItem, GiItem
from vkrb.attachment.models import Attachment


class Expert(models.Model):
    class Meta:
        verbose_name = 'Эксперт'
        verbose_name_plural = 'Эксперты'
        ordering = ('order',)

    gi = models.ForeignKey(GiItem,
                           null=True,
                           on_delete=models.CASCADE,
                           verbose_name='ГИ')
    si = ChainedForeignKey(SiItem,
                           null=True,
                           chained_field="gi",
                           chained_model_field="gi",
                           show_all=False,
                           auto_choose=True,
                           sort=False,
                           verbose_name='СИ'
                           )
    specialty = models.ForeignKey('recourse.Specialty',
                                  null=True,
                                  verbose_name='Специализация эксперта',
                                  on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, verbose_name='Имя')
    last_name = models.CharField(max_length=255, verbose_name='Фамилия')
    patronymic = models.CharField(max_length=255, verbose_name='Отчество')
    photo = models.ForeignKey(Attachment, null=True, blank=True, on_delete=models.CASCADE, verbose_name='Фото')
    info = models.TextField(verbose_name='Направление курсов')
    email = models.CharField(max_length=255, verbose_name='Email')
    order = models.PositiveIntegerField(default=0, blank=False, null=False)


    def full_name(self):
        return f'{self.last_name} {self.first_name} {self.patronymic}'

    full_name.short_description = 'ФИО'

    def __str__(self):
        return f'{self.last_name} {self.first_name} {self.patronymic}'
