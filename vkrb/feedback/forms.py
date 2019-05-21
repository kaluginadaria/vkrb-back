import requests
from django import forms
from django.urls import reverse

from vkrb.application.settings import MAILGUN_SERVER_NAME, MAILGUN_ACCESS_KEY, SENDER_EMAIL
from vkrb.core.utils import build_url, build_url_with_domain
from vkrb.feedback.models import FeedbackItem, InCharge


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = FeedbackItem
        fields = ['author', 'category', 'subject', 'text']

    def send_feedback(self):
        in_charge_email = InCharge.get_solo().email
        url = reverse(
            'admin:{0}_{1}_change'.format(self.instance._meta.app_label, self.instance._meta.model_name),
            args=(self.instance.pk,))
        admin_url = build_url_with_domain(url)
        requests.post(
            "https://api.mailgun.net/v3/{}/messages".format(MAILGUN_SERVER_NAME),
            auth=("api", MAILGUN_ACCESS_KEY),
            data={"from": f"vkrb <{SENDER_EMAIL}>",
                  "to": [in_charge_email],
                  "subject": "Письмо из формы обратной связи",
                  "text": f"Письмо из формы обратной связи:\n"
                  f"Автор: {self.cleaned_data.get('author')}\n"
                  f"Категория: {self.cleaned_data.get('category')}\n"
                  f"Тема обращения: {self.cleaned_data.get('subject')}\n"
                  f"Текст обращения: {self.cleaned_data.get('text')}\n"
                  f"Ссылка на обращение: {admin_url}"
                  })

    def save(self, commit=True):
        instance = super().save()
        self.send_feedback()
