from django_serializer.base_views import CreateView, ListView
from django_serializer.permissions import PermissionsModelMixin

from vkrb.core.mixins import LimitOffsetFullPaginator
from vkrb.feedback.forms import FeedbackForm
from vkrb.feedback.models import CategoryFeedback
from vkrb.feedback.serializers import CategoryFeedbackSerializer


class FeedbackSendView(CreateView):
    form_class = FeedbackForm
    authorized_permission = (PermissionsModelMixin.Permission.R, PermissionsModelMixin.Permission.W)
    unauthorized_permission = (PermissionsModelMixin.Permission.R, PermissionsModelMixin.Permission.W)

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        return {}


class CategoryFeedbackListView(ListView):
    authorized_permission = (PermissionsModelMixin.Permission.R,)
    unauthorized_permission = (PermissionsModelMixin.Permission.R,)
    paginator = LimitOffsetFullPaginator
    model = CategoryFeedback
    serializer = CategoryFeedbackSerializer
