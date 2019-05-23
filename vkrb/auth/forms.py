from django import forms
from django.core.exceptions import ValidationError
from django.db import transaction

from vkrb.auth.models import VerificationCode
from vkrb.core.models import User, PushToken
from vkrb.core.utils import validate_phone_number


def phone_validator(value):
    value = validate_phone_number(value)
    if not value:
        raise ValidationError('Неверный формат')
    return value


class ActivateResetForm(forms.ModelForm):
    code = forms.CharField()

    class Meta:
        model = User
        fields = (
            'email', 'password'
        )

    def clean_code(self):
        code = self.cleaned_data.get('code')
        email = self.cleaned_data.get('email')
        user, check = VerificationCode.objects.check_verification_code(VerificationCode.Type.RESTORE, email, code)
        if user and check:
            return code
        raise ValidationError('Неверный код')

    def clean_email(self):
        return self.cleaned_data.get('email')

    def save(self, commit=True):
        password = self.cleaned_data.get('password')
        user = self.instance
        user.set_password(password)
        user.save()
        return user


class RegisterForm(forms.ModelForm):
    # phone = forms.CharField(max_length=20, validators=[phone_validator])

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # domain = re.search("@.+", email).group()[1:]
        # if not AvailableDomains.objects.filter(domain=domain):
        #     raise ValidationError('К сожалению, ваш домен не включен в список доступных')
        if self.instance.pk and self.instance.is_active:
            raise ValidationError('Пользователь с таким email уже существует')
        return email

    class Meta:
        model = User
        fields = (
            'email', 'first_name', 'password'
        )

    def save(self, commit=True):
        instance = super().save(commit=False)
        recreate = self.instance.pk is not None
        instance.is_active = True
        instance.set_password(instance.password)
        instance.save()
        # VerificationCode.objects.create_verification_code(
        #     VerificationCode.Type.SIGNUP, instance, recreate=recreate
        # )
        return instance


class PushTokenForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.session = kwargs.pop('session')
        super().__init__(*args, **kwargs)

    def clean_token(self):
        token = self.cleaned_data.get('token')
        if token:
            PushToken.objects.filter(token=token).delete()
        return token

    class Meta:
        model = PushToken
        fields = ('token', 'device_type')

    def save(self, commit=True):
        with transaction.atomic():
            session_key = self.session.session_key
            PushToken.objects.filter(
                user=self.user, session_key=session_key
            ).delete()
            instance = super().save(commit=False)
            instance.user = self.user
            instance.session_key = session_key
            instance.save()
        return instance
