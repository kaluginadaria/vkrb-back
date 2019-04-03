from django_serializer.base_views import ListView, DetailsView
from django_serializer.permissions import PermissionsModelMixin

from vkrb.core.mixins import LimitOffsetFullPaginator
from vkrb.matrix.models import MatrixItem
from vkrb.matrix.serializers import MatrixSerializer, MatrixItemSerializer


class MatrixItemListView(ListView):
    section = 'matrix'
    authorized_permission = (PermissionsModelMixin.Permission.R,)
    model = MatrixItem
    serializer = MatrixSerializer
    paginator = LimitOffsetFullPaginator

    def get_queryset(self):
        return self.model.objects.filter(parent=None)


class MatrixItemGetView(DetailsView):
    authorized_permission = (PermissionsModelMixin.Permission.R,)
    model = MatrixItem
    serializer = MatrixItemSerializer
