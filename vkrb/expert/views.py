from django import forms
from django.contrib.contenttypes.models import ContentType
from django_serializer.base_views import ListView, CreateView, DeleteView
from django_serializer.exceptions import ServerError
from django_serializer.mixins import SerializerMixin
from django_serializer.permissions import PermissionsModelMixin

from vkrb.core.mixins import EventMixin, LimitOffsetFullPaginator
from vkrb.expert.models import Expert
from vkrb.expert.serializers import ExpertSerializer
from vkrb.favorites.forms import FavoriteForm
from vkrb.favorites.models import FavoriteItem


class ExpertListView(EventMixin, ListView):
    section = 'expert'
    authorized_permission = (PermissionsModelMixin.Permission.R,)
    paginator = LimitOffsetFullPaginator
    model = Expert
    serializer = ExpertSerializer

    def get_serializer_kwargs(self, obj, **kwargs):
        serializer_kwargs = super().get_serializer_kwargs(obj, **kwargs)
        serializer_kwargs['user'] = self.request.user
        return serializer_kwargs

    def get_queryset(self):
        return self.model.objects.all().order_by('order')


class FavoriteExpertCreateView(CreateView):
    authorized_permission = (PermissionsModelMixin.Permission.R,
                             PermissionsModelMixin.Permission.W)
    serializer = ExpertSerializer
    form_class = FavoriteForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['content_type'] = 'expert'
        return kwargs

    def get_serializer_kwargs(self, obj, **kwargs):
        serializer_kwargs = super().get_serializer_kwargs(obj, **kwargs)
        serializer_kwargs['user'] = self.request.user
        return serializer_kwargs

    def post(self, request, *args, **kwargs):
        inst = super().post(request, *args, **kwargs)
        return inst.content_object



class FavoriteExpertDeleteView(SerializerMixin, DeleteView):
    authorized_permission = (PermissionsModelMixin.Permission.R,
                             PermissionsModelMixin.Permission.D)
    model = FavoriteItem
    serializer = ExpertSerializer

    class FavoriteForm(forms.Form):
        object_id = forms.IntegerField()

    def get_args_form(self):
        return self.FavoriteForm

    def get_object(self):
        content_type = ContentType.objects.get(model='expert')
        try:
            return self.model.objects.get(user=self.request.user,
                                          content_type=content_type,
                                          object_id=self.request_args['object_id'])
        except self.model.DoesNotExist:
            raise ServerError(ServerError.NOT_FOUND)

    def get_serializer_kwargs(self, obj, **kwargs):
        serializer_kwargs = super().get_serializer_kwargs(obj, **kwargs)
        serializer_kwargs['user'] = self.request.user
        return serializer_kwargs

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        try:
            return Expert.objects.get(id=self.request_args['object_id'])
        except Expert.DoesNotExist:
            raise ServerError(ServerError.NOT_FOUND)
