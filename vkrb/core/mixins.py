from django.db.models import F
from django_serializer.paginator import LimitOffsetPaginator

from vkrb.popular.models import UserPopular


class EventMixin:
    section = None

    def get(self, request, *args, **kwargs):
        resp = super().get(request, *args, **kwargs)
        user = self.request.user
        if user.is_authenticated and self.section:
            popular, created = UserPopular.objects.get_or_create(
                user=user,
                section=self.section
            )
            popular.amount = F('amount') + 1
            popular.save()
        return resp


class LimitOffsetFullPaginator(LimitOffsetPaginator):
    LIMIT = None
    OFFSET = None

    def page(self):
        if self.validated_arguments is None:
            self.validate_arguments()
        offset = self.validated_arguments.get('offset', 0)
        limit = self.validated_arguments.get('limit')
        if limit and offset:
            return self.object_list[offset:offset + limit]
        elif limit and offset is None:
            return self.object_list[:limit]
        elif offset and limit is None:
            return self.object_list[offset:]
        else:
            return self.object_list
