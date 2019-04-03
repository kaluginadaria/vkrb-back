from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin, Group
from django.db import models
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from vkrb.attachment.models import Attachment
from vkrb.core.utils import build_url
from vkrb.expert.models import Expert


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    objects = UserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    email = models.EmailField('E-mail', unique=True)
    phone = models.CharField('Телефон', max_length=20, null=True, default=None)
    first_name = models.CharField('Имя', max_length=30)
    last_name = models.CharField('Фамилия', max_length=30, null=True,
                                 blank=True, default=None)

    company = models.CharField('Компания', max_length=255,
                               null=True, default=None)
    location = models.CharField('Место нахождения', max_length=255,
                                null=True, default=None)
    expert = models.ForeignKey(Expert, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Эксперт')

    photo = models.ForeignKey(
        Attachment,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Фото'
    )
    age = models.IntegerField(null=True, blank=True, verbose_name='Возраст')
    experience = models.IntegerField(null=True, blank=True, verbose_name='Стаж в компании')
    occupations = models.TextField(null=True, blank=True, verbose_name='Род деятельности')
    interests = models.TextField(null=True, blank=True, verbose_name='Интересные темы')
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log '
                    'into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'

    is_blocked = models.BooleanField(
        verbose_name='Блокировка редактирования профиля',
        default=False,

        help_text=_('Указывает на возможность изменения профиля'),
    )

    def get_full_name(self):
        return f'{self.last_name} {self.first_name}'

    def get_short_name(self):
        return self.email

    def image_tag(self):
        if self.photo:
            return mark_safe(
                '<div style="background-position: center;'
                ' background-repeat: no-repeat;'
                ' background-size: cover;'
                ' background-image: url(%s);'
                ' height: 150px;'
                ' width: 150px;" />' % build_url(self.photo.url))
        else:
            return '-'

    image_tag.short_description = 'Фото'
    image_tag.allow_tags = True


class DeviceType:
    IOS = 'ios'
    ANDROID = 'android'

    CHOICES = (
        (IOS, 'iOS'),
        (ANDROID, 'Android'),
    )


class PushToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session_key = models.CharField(max_length=255, null=True, default=None)
    device_type = models.CharField(choices=DeviceType.CHOICES,
                                   default=DeviceType.IOS, max_length=10)
    token = models.CharField(max_length=255, unique=True)

    class Meta:
        unique_together = [
            ('user', 'session_key')
        ]
