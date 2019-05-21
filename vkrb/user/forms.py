from django import forms
from django.core.exceptions import ValidationError

from vkrb.client.push import NewUserChangedItemPush
from vkrb.user.models import UserChanged, StatusType


class UserAdminChangedForm(forms.ModelForm):
    class Meta:
        model = UserChanged
        fields = ['reason', 'status', 'last_name', 'first_name',
                  'phone', 'location', 'company']

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get("status")
        reason = cleaned_data.get("reason")
        is_status_set = self.instance.is_status_set
        if not is_status_set:
            if status == StatusType.REJECTED:
                if reason in [None, '']:
                    raise ValidationError("Вы не можете отклонить"
                                          " изменения без причины")

            elif status == StatusType.APPROVED:
                if reason is not '':
                    raise ValidationError("Вы не можете указывать "
                                          "причину при подтверждении")
        else:
            raise ValidationError("Вы уже приняли решение по этой заявке")

    def save(self, commit=True):
        instance = super().save(commit)
        if not instance.status == StatusType.UNCHECKED:
            # NewUserChangedItemPush(instance).send()
            if instance.is_status_set is False:
                if instance.status == StatusType.APPROVED:
                    user = self.instance.user
                    user.age = self.instance.age
                    user.first_name = self.instance.first_name
                    user.last_name = self.instance.last_name
                    user.phone = self.instance.phone
                    user.location = self.instance.location
                    user.company = self.instance.company
                    user.photo = self.instance.photo
                    user.experience = self.instance.experience
                    user.occupations = self.instance.occupations
                    user.interests = self.instance.interests
                    user.save()

            instance.is_status_set = True
            instance.save()

        return instance


class UserClientChangedForm(forms.ModelForm):
    class Meta:
        model = UserChanged
        fields = ['last_name', 'first_name',
                  'phone', 'location', 'company',
                  'photo', 'experience',
                  'occupations', 'interests',
                  'age']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.user = self.user
        if commit:
            instance.save()

        return instance
