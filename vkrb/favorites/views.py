from django_serializer.base_views import BaseView
from django_serializer.mixins import (CsrfExemptMixin,
                                      FormMixin,
                                      SerializerMixin)
from django_serializer.permissions import PermissionsModelMixin, PermissionsMixin

from vkrb.core.mixins import LimitOffsetFullPaginator
from vkrb.favorites.models import FavoriteItem
from vkrb.favorites.serializers import FavoriteSerializer


class FavoritesListView(CsrfExemptMixin, PermissionsMixin,
                        FormMixin, SerializerMixin, BaseView):
    section = 'favorites'
    authorized_permission = (PermissionsModelMixin.Permission.R,)
    paginator = LimitOffsetFullPaginator
    model = FavoriteItem
    serializer = FavoriteSerializer

    def get_serializer_kwargs(self, obj, **kwargs):
        serializer_kwargs = super().get_serializer_kwargs(obj, **kwargs)
        serializer_kwargs['user'] = self.request.user
        return serializer_kwargs

    def get(self, request, *args, **kwargs):
        self.check_r_permission(self.request.user)
        return self.get_queryset()

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)
