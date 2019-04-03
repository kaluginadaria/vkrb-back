import random
from datetime import timedelta

import requests
from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone

from vkrb.application.settings import MAILGUN_SERVER_NAME, MAILGUN_ACCESS_KEY, SENDER_EMAIL
from vkrb.core.models import User


class VerificationCodeManager(models.Manager):
    def create_verification_code(self, code_type, user, recreate=False):
        verification_code = self.filter(
            type=code_type, user=user
        ).first()

        if verification_code and (
                recreate or verification_code.expired < timezone.now()):
            verification_code.delete()
            verification_code = None

        if not verification_code:
            if settings.DRY_RUN_VERIFICATION:
                code = settings.DEFAULT_VERIFICATION_CODE
            else:
                code = random.randint(1000, 9999)
            expired = timezone.now() + timedelta(
                seconds=settings.VERIFICATION_CODE_TIMEOUT
            )
            verification_code = self.get_or_create(
                type=code_type, user=user,
                defaults={'code': code, 'expired': expired}
            )
            response = requests.post(
                "https://api.mailgun.net/v3/{}/messages".format(MAILGUN_SERVER_NAME),
                auth=("api", MAILGUN_ACCESS_KEY),
                data={"from": "vkrb <{}>".format(SENDER_EMAIL),
                      "to": [user.email],
                      "subject": "Код для регистрации",
                      "text": "Код: {}".format(code)})

            # TODO сделать шаблоны писем

        return verification_code

    def check_verification_code(self, code_type, email, code):
        user = User.objects.filter(email=email).first()
        if not user:
            return None, False
        if code_type != VerificationCode.Type.RESTORE and user.is_active:
            return None, False
        verification_code = self.filter(user=user, code=code).first()
        if not verification_code:
            return None, False
        if verification_code.type != code_type:
            return None, False
        verification_code.delete()
        if verification_code.expired < timezone.now():
            return None, False
        return user, True


class VerificationCode(models.Model):
    objects = VerificationCodeManager()

    class Type:
        SIGNUP = 1
        RESTORE = 2

        CHOICES = (
            (SIGNUP, 'Регистрация'),
            (RESTORE, 'Восстановление')
        )

    type = models.SmallIntegerField(
        'Тип',
        choices=Type.CHOICES,
        default=Type.SIGNUP
    )
    code = models.CharField('Код', max_length=64)
    expired = models.DateTimeField('Время протухания', default=timezone.now)

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='codes'
    )

    class Meta:
        unique_together = [
            ('type', 'user')
        ]


class AvailableDomains(models.Model):
    validator = RegexValidator(r"[\w-]+(\.[\w-]+)+\.?", "Ваш домен должен быть вида google.com")
    domain = models.CharField('Домен', max_length=80,validators=[validator])

    class Meta:
        verbose_name = 'Разрешенный домен'
        verbose_name_plural = 'Разрешенные домены'

    def __str__(self):
        return f'{self.domain}'
