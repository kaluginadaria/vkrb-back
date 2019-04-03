from django.contrib import admin

from vkrb.event.forms import EventForm
from vkrb.event.models import Event, EventType


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    form = EventForm

    list_display = ('subject', 'type', 'start', 'end', 'location','pdf')
    list_filter = ('type', 'location')
    search_fields = ('subject',)
    autocomplete_fields = ('type',)


@admin.register(EventType)
class EventTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'color')
    search_fields = ('name',)
