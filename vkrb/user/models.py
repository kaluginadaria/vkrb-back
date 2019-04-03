from django.db import models

from vkrb.attachment.models import Attachment
from vkrb.core.models import User
from vkrb.expert.models import Expert


class StatusType:
    APPROVED = 'approved'
    REJECTED = 'rejected'
    UNCHECKED = 'unchecked'

    CHOICES = (
        (APPROVED, 'Подтвержден'),
        (REJECTED, 'Отклонен'),
        (UNCHECKED, 'Не рассмотрен')
    )


class UserChanged(models.Model):
    class Meta:
        verbose_name = 'Запрос на измененные данных пользователя'
        verbose_name_plural = 'Запросы на измененные данных пользователей'


    user = models.ForeignKey(User, verbose_name='Пользователь', blank=True,
                             on_delete=models.CASCADE,
                             editable=False,
                             default=None)
    photo = models.ForeignKey(
        Attachment,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Новое фото'
    )
    age = models.IntegerField(null=True, blank=True, verbose_name='Новый возраст')
    experience = models.IntegerField(null=True, blank=True, verbose_name='Новый стаж в компании')
    occupations = models.TextField(null=True, blank=True, verbose_name='Новый род деятельности')
    interests = models.TextField(null=True, blank=True, verbose_name='Новые интересные темы')
    phone = models.CharField('Новый телефон', max_length=20,
                             null=True, default=None)
    first_name = models.CharField('Новое имя', max_length=30)
    last_name = models.CharField('Новая фамилия', max_length=30, null=True,
                                 blank=True, default=None)

    company = models.CharField('Новая компания', max_length=255,
                               null=True, default=None)
    location = models.CharField('Новое местонахождение', max_length=255,
                                null=True, default=None)

    status = models.CharField(max_length=10, choices=StatusType.CHOICES,
                              default=StatusType.UNCHECKED,
                              verbose_name='Статус заявки на изменение профиля')

    reason = models.TextField(null=True, blank=True,
                              verbose_name='Причина отклонения')

    created_date = models.DateTimeField(auto_now_add=True)

    is_status_set = models.BooleanField(default=False)



    def get_full_name(self):
        return f'{self.last_name} {self.first_name}'

    def get_short_name(self):
        return self.user.email

    def __str__(self):
        return self.user.email