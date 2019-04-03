from django.contrib.admin import SimpleListFilter
from django.db.models import Q


class AnsweredFilter(SimpleListFilter):
    title = 'Есть ответ'
    parameter_name = 'answer'

    def lookups(self, request, model_admin):
        return [(False, u'Нет'), (True, u'Да')]

    def queryset(self, request, queryset):
        if self.value() is None:
            return queryset
        elif self.value() == 'True':
            return queryset.exclude(Q(answer=None) | Q(answer=''))
        else:
            return queryset.filter(Q(answer=None) | Q(answer=''))
