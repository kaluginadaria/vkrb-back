import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.forms import BaseInlineFormSet

from vkrb.recourse.models import Recourse, RecourseLike


class RecourseForm(forms.ModelForm):
    class Meta:
        model = Recourse
        fields = ['subject',
                  'question', 'parent']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def clean_parent(self):
        parent = self.cleaned_data.get('parent')
        if parent:
            if parent.parent_id is None:
                return parent
            raise ValidationError('Нельзя привязать к обсуждению')

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.user = self.user
        if commit:
            instance.save()

        return instance


class LikeRecourseForm(forms.ModelForm):
    class Meta:
        model = RecourseLike
        fields = ['recourse']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def clean_recourse(self):
        recourse = self.cleaned_data.get('recourse')
        try:
            RecourseLike.objects.get(user=self.user, recourse=recourse)
            raise ValidationError('Пользователь уже поставил лайк')
        except RecourseLike.DoesNotExist:
            qs = Q(recourse__parent=recourse) | Q(recourse__pk=recourse.pk)
            if recourse.parent:
                qs |= Q(recourse__pk=recourse.parent.pk) | Q(recourse__parent=recourse.parent)
            count = RecourseLike.objects.filter(Q(user=self.user) & qs).count()

            if count >= 5:
                raise ValidationError('Нельзя поставить лайк более 5 раз')

            return recourse

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.user = self.user
        if commit:
            instance.save()

        return instance


class RecourseInlineForm(BaseInlineFormSet):

    def save_existing_objects(self, commit=True):
        self.changed_objects = []
        self.deleted_objects = []
        if not self.initial_forms:
            return []

        saved_instances = []
        forms_to_delete = self.deleted_forms
        for form in self.initial_forms:
            obj = form.instance
            # If the pk is None, it means either:
            # 1. The object is an unexpected empty model, created by invalid
            #    POST data such as an object outside the formset's queryset.
            # 2. The object was already deleted from the database.
            if obj.pk is None:
                continue
            if form in forms_to_delete:
                self.deleted_objects.append(obj)
                self.delete_existing(obj, commit=commit)
            elif form.has_changed():
                if 'answer' in form.changed_data:
                    expert = self.user.expert
                    old_answer = form.initial.get('answer')
                    if expert and old_answer in ['', None] and obj.reaction_date is None:
                        obj.reaction_date = datetime.datetime.now()
                        # NewRecourseAnswerPush(obj).send()
                    if obj.expert is None and expert:
                        obj.expert = expert
                self.changed_objects.append((obj, form.changed_data))
                saved_instances.append(self.save_existing(form, obj, commit=commit))
                if not commit:
                    self.saved_forms.append(form)
        return saved_instances
