from django import forms
from django.contrib.contenttypes.models import ContentType
from django_serializer.base_views import ListView, CreateView, DeleteView, DetailsView
from django_serializer.exceptions import ServerError
from django_serializer.permissions import PermissionsModelMixin

from vkrb.activity.models import GiItem, SiItem
from vkrb.activity.serializers import ActivityGiItemSerializer, ActivitySiItemSerializer, \
    ShortActivitySiItemSerializer, ShortActivityGiItemSerializer
from vkrb.core.mixins import LimitOffsetFullPaginator
from vkrb.favorites.forms import FavoriteForm
from vkrb.favorites.models import FavoriteItem


class GiListView(ListView):
    authorized_permission = (PermissionsModelMixin.Permission.R,)
    unauthorized_permission = (PermissionsModelMixin.Permission.R,)
    paginator = LimitOffsetFullPaginator
    model = GiItem
    serializer = ShortActivityGiItemSerializer

    def get_serializer_kwargs(self, obj, **kwargs):
        serializer_kwargs = super().get_serializer_kwargs(obj, **kwargs)
        serializer_kwargs['user'] = self.request.user
        return serializer_kwargs




class SiListView(ListView):
    authorized_permission = (PermissionsModelMixin.Permission.R,)
    unauthorized_permission = (PermissionsModelMixin.Permission.R,)
    paginator = LimitOffsetFullPaginator
    model = SiItem
    serializer = ShortActivitySiItemSerializer

    def get_serializer_kwargs(self, obj, **kwargs):
        serializer_kwargs = super().get_serializer_kwargs(obj, **kwargs)
        serializer_kwargs['user'] = self.request.user
        return serializer_kwargs


class FavoriteGiCreateView(CreateView):
    authorized_permission = (PermissionsModelMixin.Permission.R, PermissionsModelMixin.Permission.W)
    serializer = ActivityGiItemSerializer
    form_class = FavoriteForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['content_type'] = 'giitem'

        return kwargs

    def get_serializer_kwargs(self, obj, **kwargs):
        serializer_kwargs = super().get_serializer_kwargs(obj, **kwargs)
        serializer_kwargs['user'] = self.request.user
        return serializer_kwargs

    def post(self, request, *args, **kwargs):
        inst = super().post(request, *args, **kwargs)
        return inst.content_object


class FavoriteSiCreateView(CreateView):
    authorized_permission = (PermissionsModelMixin.Permission.R, PermissionsModelMixin.Permission.W)
    serializer = ActivitySiItemSerializer
    form_class = FavoriteForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['content_type'] = 'siitem'
        return kwargs

    def get_serializer_kwargs(self, obj, **kwargs):
        serializer_kwargs = super().get_serializer_kwargs(obj, **kwargs)
        serializer_kwargs['user'] = self.request.user
        return serializer_kwargs

    def post(self, request, *args, **kwargs):
        inst = super().post(request, *args, **kwargs)
        return inst.content_object


class FavoriteGiDeleteView(DeleteView):
    authorized_permission = (PermissionsModelMixin.Permission.R, PermissionsModelMixin.Permission.D)
    model = FavoriteItem

    class FavoriteForm(forms.Form):
        object_id = forms.IntegerField()

    def get_args_form(self):
        return self.FavoriteForm

    def get_object(self):
        content_type = ContentType.objects.get(model='giitem')
        try:
            return self.model.objects.get(user=self.request.user,
                                          content_type=content_type,
                                          object_id=self.request_args['object_id'])
        except self.model.DoesNotExist:
            raise ServerError(ServerError.NOT_FOUND)


class FavoriteSiDeleteView(DeleteView):
    authorized_permission = (PermissionsModelMixin.Permission.R, PermissionsModelMixin.Permission.D)
    model = FavoriteItem

    class FavoriteForm(forms.Form):
        object_id = forms.IntegerField()

    def get_args_form(self):
        return self.FavoriteForm

    def get_object(self):
        content_type = ContentType.objects.get(model='siitem')
        try:
            return self.model.objects.get(user=self.request.user,
                                          content_type=content_type,
                                          object_id=self.request_args['object_id'])
        except self.model.DoesNotExist:
            raise ServerError(ServerError.NOT_FOUND)


class GiGetView(DetailsView):
    authorized_permission = (PermissionsModelMixin.Permission.R,)
    unauthorized_permission = (PermissionsModelMixin.Permission.R,)
    model = GiItem
    serializer = ActivityGiItemSerializer

    def get_serializer_kwargs(self, obj, **kwargs):
        serializer_kwargs = super().get_serializer_kwargs(obj, **kwargs)
        serializer_kwargs['user'] = self.request.user
        return serializer_kwargs


class SiGetView(DetailsView):
    authorized_permission = (PermissionsModelMixin.Permission.R,)
    unauthorized_permission = (PermissionsModelMixin.Permission.R,)
    model = SiItem
    serializer = ActivitySiItemSerializer

    def get_serializer_kwargs(self, obj, **kwargs):
        serializer_kwargs = super().get_serializer_kwargs(obj, **kwargs)
        serializer_kwargs['user'] = self.request.user
        return serializer_kwargs
