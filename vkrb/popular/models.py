from django.db import models

from vkrb.core.models import User


class UserPopular(models.Model):
    class Meta:
        verbose_name = 'популярная категория пользователя'
        verbose_name_plural = 'популярные категории пользователей'
        unique_together = ('user', 'section')

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Название категории')
    section = models.CharField(max_length=255, verbose_name='Название категории')
    amount = models.PositiveIntegerField(default=0, blank=False, null=False)

    def __str__(self):
        return self.section
