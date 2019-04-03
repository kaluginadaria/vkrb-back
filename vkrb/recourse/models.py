from django.core.validators import URLValidator
from django.db import models
from django_serializer.permissions import PermissionsModelMixin
from smart_selects.db_fields import ChainedForeignKey

from vkrb.activity.models import SiItem, GiItem
from vkrb.attachment.models import Attachment


class Specialty(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название специализации')
    icon = models.ForeignKey(Attachment, verbose_name=u'Иконка', on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0, blank=False, null=False,
                                        verbose_name='Порядок')

    class Meta:
        verbose_name = 'Специализация'
        verbose_name_plural = 'Специализации'
        ordering = ('order',)

    def __str__(self):
        return self.title


class Recourse(models.Model):
    user = models.ForeignKey('core.User', on_delete=models.CASCADE, verbose_name='Автор')
    parent = models.ForeignKey("Recourse", on_delete=models.CASCADE, blank=True, null=True)
    specialty = models.ForeignKey(Specialty, verbose_name='Специализация обращения', on_delete=models.CASCADE)
    gi = models.ForeignKey(GiItem, null=True, on_delete=models.CASCADE, verbose_name='ГИ')
    si = ChainedForeignKey(SiItem,
                           null=True,
                           chained_field="gi",
                           chained_model_field="gi",
                           show_all=False,
                           auto_choose=True,
                           sort=False,
                           verbose_name='СИ')
    expert = models.ForeignKey('expert.Expert', null=True, blank=True, verbose_name='Эксперт', on_delete=models.CASCADE)
    subject = models.CharField(max_length=255, verbose_name='Тема обращения')
    question = models.TextField(verbose_name='Текст обращения')
    answer = models.TextField(null=True, blank=True,
                              verbose_name='Ответ эксперта')
    link = models.TextField(null=True, validators=[URLValidator()],
                            verbose_name='Ссылка на официальный документ')
    photo = models.ForeignKey(Attachment, null=True,
                              blank=True,
                              verbose_name='Прикрепить фото к ответу эксперта',
                              on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True,
                                   verbose_name='Дата публикации вопроса')
    reaction_date = models.DateTimeField(null=True, blank=True,
                                         verbose_name='Дата и время реакции')
    keywords = models.TextField(verbose_name='Ключевые слова', null=True, blank=True, help_text='Через пробел')

    class Meta:
        verbose_name = 'Обсуждение'
        verbose_name_plural = 'Обсуждения'

    def __str__(self):
        return f'{self.specialty} - {self.subject}'

    def get_likes(self):
        count = RecourseLike.objects.filter(recourse_id=self.pk).count()
        return count

    def get_text_for_search_vector(self):
        return ' '.join(filter(lambda v: bool(v), [
            self.question, self.answer, self.subject, self.keywords
        ]))


class RecourseLike(PermissionsModelMixin, models.Model):
    group_permission = (PermissionsModelMixin.Permission.R,)
    authorized_permission = ()

    user = models.ForeignKey('core.User', on_delete=models.CASCADE, verbose_name='Автор')
    recourse = models.ForeignKey(Recourse, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'
        unique_together = ('user', 'recourse')

    def is_owner(self, user):
        return self.user == user
