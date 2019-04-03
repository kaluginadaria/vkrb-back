from django.contrib import admin

from vkrb.auth.models import AvailableDomains


@admin.register(AvailableDomains)
class DomainsAdmin(admin.ModelAdmin):
    list_display = ('domain',)
    search_fields = ('domain',)
