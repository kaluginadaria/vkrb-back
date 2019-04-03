import datetime

from adminsortable2.admin import SortableAdminMixin
from django.contrib import admin
from django.db.models import Q

from vkrb.client.push import NewRecourseAnswerPush
from vkrb.recourse.filters import AnsweredFilter
from vkrb.recourse.forms import RecourseInlineForm
from vkrb.recourse.models import Recourse, Specialty


class RecourseInline(admin.TabularInline):
    model = Recourse
    extra = 0
    formset = RecourseInlineForm
    readonly_fields = ('expert',)
    exclude = ('keywords',)

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        formset.user = request.user
        return formset


@admin.register(Recourse)
class RecourseAdmin(admin.ModelAdmin):
    list_display = ('subject', 'specialty', 'created', 'user', 'comments', 'answered')
    exclude = ('parent',)
    inlines = (RecourseInline,)
    list_filter = (AnsweredFilter,)
    search_fields = ('subject',)
    readonly_fields = ('expert',)
    autocomplete_fields = ('specialty', 'user')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        conditions = [Q(parent__isnull=True)]
        expert = request.user.expert
        if expert is not None and request.user.is_superuser is False:
            conditions.extend([Q(specialty=expert.specialty), Q(si=expert.si)])

        return qs.filter(*conditions)

    def answered(self, obj):
        return True if obj.answer else False

    def comments(self, obj):
        count = Recourse.objects.filter(parent_id=obj.id).count()
        return count

    def save_model(self, request, obj, form, change):
        user = request.user
        if user.expert is not None and change and 'answer' in form.changed_data:
            old_answer = form.initial.get('answer')
            new_answer = form.cleaned_data.get('answer')
            if new_answer != old_answer:
                obj.expert = user.expert
                if obj.reaction_date is None:
                    obj.reaction_date = datetime.datetime.now()
                    NewRecourseAnswerPush(obj).send()
        obj.save()

    comments.short_description = 'Кол-во комментариев'
    answered.short_description = 'Есть ответ'
    answered.boolean = True


@admin.register(Specialty)
class SpecialtyAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('name',)
