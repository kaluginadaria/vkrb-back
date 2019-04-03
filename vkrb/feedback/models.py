from django.db import models
from solo.models import SingletonModel

from vkrb.core.models import User


class CategoryFeedback(models.Model):
    class Meta:
        verbose_name = 'Категория обращения'
        verbose_name_plural = 'Категории обращения'

    title = models.CharField(max_length=255, verbose_name='Название категории')

    def __str__(self):
        return self.title


class FeedbackItem(models.Model):
    author = models.EmailField(verbose_name='E-mail автора обращения')
    category = models.ForeignKey(CategoryFeedback, verbose_name='Категория', on_delete=models.CASCADE)
    subject = models.CharField(max_length=255, verbose_name='Тема обращения')
    text = models.TextField(verbose_name='Текст обращения')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время обращения')
    is_seen = models.BooleanField(default=False, verbose_name='Просмотренно')

    class Meta:
        verbose_name = 'Обращение к разработчику'
        verbose_name_plural = 'Обращения к разработчику'

    def __str__(self):
        return f'{self.category} - {self.subject}'


class InCharge(SingletonModel):
    email = models.EmailField(unique=True, verbose_name='E-mail отвественного за обращения')

    def __str__(self):
        return u"Ответственный за обращения"

    class Meta:
        verbose_name = "Ответственный за обращения"

