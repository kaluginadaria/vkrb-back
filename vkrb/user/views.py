from django import forms
from django_serializer.base_views import DetailsView, BaseView, CreateView
from django_serializer.exceptions import ServerError
from django_serializer.mixins import CsrfExemptMixin
from django_serializer.permissions import PermissionsModelMixin, PermissionsMixin

from vkrb.core.models import User
from vkrb.core.serializers import UserSerializer
from vkrb.settings.models import SiteConfiguration
from vkrb.user.forms import UserClientChangedForm
from vkrb.user.models import UserChanged, StatusType


class UserView(DetailsView):
    authorized_permission = (PermissionsModelMixin.Permission.R,)
    serializer = UserSerializer
    model = User

    class UserFormEmptyid(forms.Form):
        id = forms.IntegerField(required=False)

    def get_args_form(self):
        return self.UserFormEmptyid

    def get_object(self):
        if self.request_args.get('id') is None:
            return self.request.user

        return super(UserView, self).get_object()

    def post(self, request, *args, **kwargs):
        raise ServerError(ServerError.NOT_IMPLEMENTED)


class UserUpdateView(CreateView):
    form_class = UserClientChangedForm
    authorized_permission = (PermissionsModelMixin.Permission.R, PermissionsModelMixin.Permission.W)

    serializer = UserSerializer

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        return self.request.user


class UserUpdatePermsView(CsrfExemptMixin, PermissionsMixin, BaseView):
    authorized_permission = (PermissionsModelMixin.Permission.R,)

    def get(self, request, *args, **kwargs):
        self.check_r_permission(self.request.user)
        is_user_blocked = request.user.is_blocked
        global_block = SiteConfiguration.objects.get().block_changes
        moderating = UserChanged.objects.filter(user=request.user,
                                                status=StatusType.UNCHECKED) \
            .exists()
        if moderating:
            return {'status_upd': 'moderating'}
        if not global_block and not is_user_blocked:
            return {'status_upd': 'opened'}
        else:
            return {'status_upd': 'closed'}
