from adminsortable2.admin import SortableAdminMixin
from django.contrib import admin

from vkrb.expert.models import Expert


# @admin.register(Expert)
# class ExpertAdmin(SortableAdminMixin, admin.ModelAdmin):
#     list_display = ('full_name', 'gi', 'si', 'info', 'email')
#     search_fields = ('first_name', 'last_name', 'patronymic', 'speciality')
#     list_filter = ('specialty',)
