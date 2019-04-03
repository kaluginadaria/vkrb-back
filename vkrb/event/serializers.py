from django_serializer.serializer.base import ModelSerializer
from django_serializer.serializer.fields import SerializerField

from vkrb.attachment.serializers import AttachmentSerializer
from vkrb.event.models import Event, EventType


class EventTypeSerializer(ModelSerializer):
    color = SerializerField(source='get_color')

    class Meta:
        model = EventType
        exclude = ('color',)

    def get_color(self, obj):
        return obj.color


class EventSerializer(ModelSerializer):
    type = SerializerField(source='get_event_type')
    pdf = SerializerField(source='get_pdf')

    class Meta:
        model = Event
        exclude = ('pdf_id',)

    def get_event_type(self, obj):
        return EventTypeSerializer(obj.type).serialize()

    def get_pdf(self, obj):
        return AttachmentSerializer(obj.pdf).serialize()
