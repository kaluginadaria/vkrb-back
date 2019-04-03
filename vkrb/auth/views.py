import json

from django import forms
from django.http import HttpResponse
from django.views import View

from django_serializer.base_views import BaseView, CreateView
from django_serializer.exceptions import FormException, ServerError
from django_serializer.mixins import SerializerMixin, CsrfExemptMixin, FormMixin, ObjectMixin
from oauth2_provider.oauth2_backends import OAuthLibCore
from oauth2_provider.oauth2_validators import OAuth2Validator
from oauth2_provider.settings import oauth2_settings

from vkrb.auth.forms import RegisterForm, ActivateResetForm, PushTokenForm
from vkrb.auth.models import VerificationCode
from vkrb.core.models import User
from vkrb.core.serializers import UserSerializer, PushTokenSerializer


class RegisterView(CsrfExemptMixin, FormMixin, SerializerMixin, BaseView):
    class EmailForm(forms.Form):
        email = forms.EmailField()

    args_form = EmailForm
    form_class = RegisterForm
    serializer = UserSerializer

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = User.objects.filter(
            email=self.request_args['email']
        ).first()
        return kwargs

    def post(self, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            instance = form.save()
        else:
            raise FormException(form)
        return instance


class Validator(OAuth2Validator):
    def validate_user(self, username, password, client, request, *args, **kwargs):
        user, verified = VerificationCode.objects.check_verification_code(
            VerificationCode.Type.SIGNUP, username, password
        )
        if verified:
            user.is_active = True
            user.save()
            request.user = user
        return user


class OAuthCore(OAuthLibCore):
    def __init__(self, server=None):
        self.server = server or oauth2_settings.OAUTH2_SERVER_CLASS(Validator())

    def _extract_params(self, request):
        uri, http_method, _, headers = super()._extract_params(request)
        try:
            data = json.loads(request.body.decode('utf-8'))
        except Exception:
            data = {}
        email = data.get('email', '')
        code = data.get('code', '')

        body = f'grant_type=password&username={email}&password={code}'
        return uri, http_method, body, headers


class ResetPasswordView(CsrfExemptMixin, BaseView):
    class EmailForm(forms.Form):
        email = forms.EmailField()

    args_form = EmailForm

    def post(self, *args, **kwargs):
        email = self.request_args['email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise ServerError(ServerError.NOT_FOUND)

        VerificationCode.objects.create_verification_code(
            VerificationCode.Type.RESTORE, user)
        return {}


class NewPasswordView(CsrfExemptMixin, ObjectMixin, FormMixin, SerializerMixin, BaseView):
    form_class = ActivateResetForm
    model = User

    class ActivateForm(forms.Form):
        email = forms.EmailField()
        code = forms.CharField()
        password = forms.CharField()

    def get_args_form(self):
        return self.ActivateForm

    def get_object(self):
        try:
            return self.model.objects.get(email=self.request_args['email'])
        except self.model.DoesNotExist:
            raise ServerError(ServerError.NOT_FOUND)
        except (ValueError, KeyError):
            raise ServerError(ServerError.BAD_REQUEST)

    def post(self, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.save()
        else:
            raise FormException(form)
        return {}


class ActivateView(CsrfExemptMixin, View):
    def post(self, *args, **kwargs):
        core = OAuthCore()
        url, headers, body, status = core.create_token_response(self.request)
        response = HttpResponse(content=body or "", status=status)

        for k, v in headers.items():
            response[k] = v

        return response


class SaveTokenView(CreateView):
    form_class = PushTokenForm
    serializer = PushTokenSerializer

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['session'] = self.request.session
        return kwargs