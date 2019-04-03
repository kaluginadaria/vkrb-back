from datetime import datetime, timezone, timedelta
from django import forms
from django.db.models import Q
from django.utils.timezone import now
from django_serializer.base_views import ListView
from django_serializer.permissions import PermissionsModelMixin

from vkrb.application import settings
from vkrb.core.mixins import EventMixin, LimitOffsetFullPaginator
from vkrb.event.models import Event, EventType
from vkrb.event.serializers import EventSerializer, EventTypeSerializer


class EventListView(EventMixin, ListView):
    class EventForm(forms.Form):
        start = forms.IntegerField(required=True)
        end = forms.IntegerField(required=True)
        nearest = forms.BooleanField(required=False)

    def get_queryset(self):
        nearest = self.request_args.get('nearest')
        if nearest:
            start = now()
            end = (now() + timedelta(weeks=2))
        else:
            start = datetime.fromtimestamp(self.request_args['start'], tz=timezone.utc)
            end = datetime.fromtimestamp(self.request_args['end'], tz=timezone.utc)

        queryset = Event.objects.filter(
            Q(
                Q(start__gte=start) &
                Q(start__lte=end)
            ) |
            Q(
                Q(end__gte=start) &
                Q(end__lte=end)
            ) |
            Q(
                Q(start__lte=start) &
                Q(end__gte=end)
            )
        ).order_by('-start')

        if nearest:
            return queryset[:settings.EVENT_NEAREST_LIMIT]
        else:
            return queryset

    args_form = EventForm
    authorized_permission = (PermissionsModelMixin.Permission.R,)
    paginator = LimitOffsetFullPaginator
    model = Event
    serializer = EventSerializer


class EventTypeListView(ListView):
    model = EventType
    serializer = EventTypeSerializer
    paginator = LimitOffsetFullPaginator
