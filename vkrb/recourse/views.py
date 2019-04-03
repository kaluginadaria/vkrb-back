from django import forms
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q, Count
from django_serializer.base_views import (ListView, DetailsView,
                                          CreateView, DeleteView, BaseView)
from django_serializer.exceptions import ServerError
from django_serializer.mixins import ObjectMixin, SerializerMixin
from django_serializer.permissions import PermissionsModelMixin, PermissionsMixin

from vkrb.core.mixins import EventMixin, LimitOffsetFullPaginator
from vkrb.core.utils import get_absolute_bundle_urls, render_to_pdf
from vkrb.favorites.forms import FavoriteForm
from vkrb.favorites.models import FavoriteItem
from vkrb.recourse.forms import RecourseForm, LikeRecourseForm
from vkrb.recourse.models import Recourse, Specialty, RecourseLike
from vkrb.recourse.serializers import (RecourseSerializer,
                                           SpecialtySerializer,
                                           RecourseLikeSerializer)


class RecourseListView(EventMixin, ListView):
    class RecourseForm(forms.Form):
        my = forms.BooleanField(required=False)
        specialty = forms.ModelChoiceField(Specialty.objects.all(), required=False)

    def get_queryset(self):
        queryset = super().get_queryset()
        q = Q(parent__isnull=True)
        my = self.request_args.get('my')
        specialty = self.request_args.get('specialty')
        if my:
            q &= Q(user=self.request.user)
        if specialty:
            q &= Q(specialty=specialty)

        return queryset.filter(q).order_by('-created')

    def get_serializer_kwargs(self, obj, **kwargs):
        serializer_kwargs = super().get_serializer_kwargs(obj, **kwargs)
        serializer_kwargs['request_user'] = self.request.user
        return serializer_kwargs

    section = 'recourse'
    args_form = RecourseForm
    authorized_permission = (PermissionsModelMixin.Permission.R,)
    paginator = LimitOffsetFullPaginator
    model = Recourse
    serializer = RecourseSerializer


class RecourseGetView(DetailsView):
    authorized_permission = (PermissionsModelMixin.Permission.R,)
    model = Recourse
    serializer = RecourseSerializer

    def get_serializer_kwargs(self, obj, **kwargs):
        serializer_kwargs = super().get_serializer_kwargs(obj, **kwargs)
        serializer_kwargs['request_user'] = self.request.user
        return serializer_kwargs


class RecourseCreateView(CreateView):
    authorized_permission = (PermissionsModelMixin.Permission.R,
                             PermissionsModelMixin.Permission.W)

    serializer = RecourseSerializer
    form_class = RecourseForm

    def get_serializer_kwargs(self, obj, **kwargs):
        serializer_kwargs = super().get_serializer_kwargs(obj, **kwargs)
        serializer_kwargs['request_user'] = self.request.user
        return serializer_kwargs

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class SpecialtyListView(ListView):
    model = Specialty
    serializer = SpecialtySerializer
    paginator = LimitOffsetFullPaginator

    def get_queryset(self):
        q = super().get_queryset()
        return q.order_by('order')


class LikeCreateView(CreateView):
    authorized_permission = (PermissionsModelMixin.Permission.R,
                             PermissionsModelMixin.Permission.W)

    serializer = RecourseLikeSerializer
    form_class = LikeRecourseForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class LikeDeleteView(DeleteView):
    class LikeForm(forms.Form):
        recourse = forms.ModelChoiceField(Recourse.objects.all())

    model = RecourseLike

    def get_args_form(self):
        return self.LikeForm

    def get_object(self):
        try:
            return self.model.objects.get(user=self.request.user,
                                          recourse=self.request_args['recourse'])
        except self.model.DoesNotExist:
            raise ServerError(ServerError.NOT_FOUND)


class CreatePDFView(ObjectMixin, PermissionsMixin, BaseView):
    model = Recourse
    authorized_permission = (PermissionsModelMixin.Permission.R,)

    def response_wrapper(self, response):
        return response

    def get(self, request, *args, **kwargs):
        self.check_r_permission(self.request.user)
        recourse = self.get_object()
        children = Recourse.objects.filter(parent=recourse) \
                       .annotate(num_likes=Count('recourselike')).order_by('-num_likes')[:5]
        ctx = {
            'recourse': recourse,
            'children': children,
            'css_urls': get_absolute_bundle_urls('pdf', 'css'),
        }
        return render_to_pdf(template_path='recourse.html', ctx=ctx)


class FavoriteRecourseCreateView(CreateView):
    authorized_permission = (PermissionsModelMixin.Permission.R,
                             PermissionsModelMixin.Permission.W)
    serializer = RecourseSerializer
    form_class = FavoriteForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['content_type'] = 'recourse'
        return kwargs

    def get_serializer_kwargs(self, obj, **kwargs):
        serializer_kwargs = super().get_serializer_kwargs(obj, **kwargs)
        serializer_kwargs['request_user'] = self.request.user
        return serializer_kwargs

    def post(self, request, *args, **kwargs):
        inst = super().post(request, *args, **kwargs)
        return inst.content_object


class FavoriteRecourseDeleteView(SerializerMixin, DeleteView):
    authorized_permission = (PermissionsModelMixin.Permission.R,
                             PermissionsModelMixin.Permission.D)
    model = FavoriteItem
    serializer = RecourseSerializer

    class FavoriteForm(forms.Form):
        object_id = forms.IntegerField()

    def get_args_form(self):
        return self.FavoriteForm

    def get_object(self):
        content_type = ContentType.objects.get(model='recourse')
        try:
            return self.model.objects.get(user=self.request.user,
                                          content_type=content_type,
                                          object_id=self.request_args['object_id'])
        except self.model.DoesNotExist:
            raise ServerError(ServerError.NOT_FOUND)

    def get_serializer_kwargs(self, obj, **kwargs):
        serializer_kwargs = super().get_serializer_kwargs(obj, **kwargs)
        serializer_kwargs['request_user'] = self.request.user
        return serializer_kwargs

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        try:
            return Recourse.objects.get(id=self.request_args['object_id'])
        except Recourse.DoesNotExist:
            raise ServerError(ServerError.NOT_FOUND)
