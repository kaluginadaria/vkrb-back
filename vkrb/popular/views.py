from django_serializer.base_views import ListView
from django_serializer.permissions import PermissionsModelMixin

from vkrb.application import settings
from vkrb.core.mixins import LimitOffsetFullPaginator
from vkrb.popular.serializers import UserPopularSerializer
from vkrb.popular.models import UserPopular


class PopularListView(ListView):
    authorized_permission = (PermissionsModelMixin.Permission.R,)
    paginator = LimitOffsetFullPaginator
    model = UserPopular
    serializer = UserPopularSerializer

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user).order_by('-amount')[:settings.POPULAR_LIST_LIMIT]
