from django import forms
from django.core.exceptions import ValidationError

from vkrb.event.models import Event


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get('start')
        end = cleaned_data.get('end')
        if start and end and start >= end:
            raise ValidationError({'start': 'Старт события должен быть раньше '
                                            'чем конец события'})
        return cleaned_data
