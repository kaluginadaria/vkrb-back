from django import forms
from django_serializer.base_views import DetailsView
from django_serializer.exceptions import ServerError

from vkrb.text.models import Text
from vkrb.text.serializers import TextSerializer


class TextGetView(DetailsView):
    model = Text
    serializer = TextSerializer

    class TypeForm(forms.Form):
        type = forms.CharField()

    def get_args_form(self):
        return self.TypeForm

    def check_permission(self, user, permission):
        return

    def get_object(self):
        type = self.request_args['type']
        try:
            return self.model.objects.get(type=type)
        except self.model.DoesNotExist:
            raise ServerError(ServerError.NOT_FOUND)
