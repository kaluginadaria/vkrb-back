from django import forms
from django.contrib.contenttypes.models import ContentType
from django_serializer.base_views import (ListView, DetailsView, BaseView,
                                          CreateView, DeleteView)
from django_serializer.exceptions import ServerError
from django_serializer.mixins import ObjectMixin, SerializerMixin
from django_serializer.paginator import LimitOffsetPaginator
from django_serializer.permissions import PermissionsModelMixin, PermissionsMixin

from vkrb.core.mixins import LimitOffsetFullPaginator
from vkrb.core.utils import get_absolute_bundle_urls, render_to_pdf
from vkrb.digest.models import DigestCategory, Digest, Article
from vkrb.digest.serializers import DigestCategorySerializer, \
    DigestSerializer, ShortArticleSerializer, ArticleSerializer
from vkrb.favorites.forms import FavoriteForm
from vkrb.favorites.models import FavoriteItem


class DigestCategoryListView(ListView):
    authorized_permission = (PermissionsModelMixin.Permission.R,)
    paginator = LimitOffsetFullPaginator
    model = DigestCategory
    serializer = DigestCategorySerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by('order')


class DigestListView(ListView):
    class DigestListForm(forms.Form):
        category = forms.ModelChoiceField(queryset=DigestCategory.objects.all(),
                                          required=False)

    args_form = DigestListForm
    authorized_permission = (PermissionsModelMixin.Permission.R,)
    paginator = LimitOffsetFullPaginator
    model = Digest
    serializer = DigestSerializer

    def get_serializer_kwargs(self, obj, **kwargs):
        serializer_kwargs = super().get_serializer_kwargs(obj, **kwargs)
        serializer_kwargs['user'] = self.request.user
        return serializer_kwargs

    def get_queryset(self):
        queryset = super().get_queryset()

        c = self.request_args.get('category')
        if c:
            queryset = queryset.filter(category=c)

        return queryset.order_by('order')


class ArticleListView(ListView):
    class ArticleListForm(forms.Form):
        digest = forms.ModelChoiceField(queryset=Digest.objects.all(),
                                        required=False)

    args_form = ArticleListForm
    authorized_permission = (PermissionsModelMixin.Permission.R,)
    paginator = LimitOffsetFullPaginator
    model = Article
    serializer = ShortArticleSerializer

    def get_serializer_kwargs(self, obj, **kwargs):
        serializer_kwargs = super().get_serializer_kwargs(obj, **kwargs)
        serializer_kwargs['user'] = self.request.user
        return serializer_kwargs

    def get_queryset(self):
        queryset = super().get_queryset()

        d = self.request_args.get('digest')
        if d:
            queryset = queryset.filter(digest=d)

        return queryset


class ArticleGetView(DetailsView):
    authorized_permission = (PermissionsModelMixin.Permission.R,)
    model = Article
    serializer = ArticleSerializer

    def get_serializer_kwargs(self, obj, **kwargs):
        serializer_kwargs = super().get_serializer_kwargs(obj, **kwargs)
        serializer_kwargs['user'] = self.request.user
        return serializer_kwargs


class CreatePDFView(ObjectMixin, PermissionsMixin, BaseView):
    model = Article
    authorized_permission = (PermissionsModelMixin.Permission.R,)

    def response_wrapper(self, response):
        return response

    def get(self, request, *args, **kwargs):
        self.check_r_permission(self.request.user)
        article = self.get_object()
        photos = article.attachments.all()
        ctx = {
            'article': article,
            'photos': photos,
            'css_urls': get_absolute_bundle_urls('pdf', 'css'),
        }
        return render_to_pdf(template_path='digest.html', ctx=ctx)


class FavoriteDigestCreateView(CreateView):
    authorized_permission = (PermissionsModelMixin.Permission.R,
                             PermissionsModelMixin.Permission.W)
    serializer = DigestSerializer
    form_class = FavoriteForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['content_type'] = 'digest'
        return kwargs

    def get_serializer_kwargs(self, obj, **kwargs):
        serializer_kwargs = super().get_serializer_kwargs(obj, **kwargs)
        serializer_kwargs['user'] = self.request.user
        return serializer_kwargs

    def post(self, request, *args, **kwargs):
        inst = super().post(request, *args, **kwargs)
        return inst.content_object


class FavoriteArticleCreateView(CreateView):
    authorized_permission = (PermissionsModelMixin.Permission.R,
                             PermissionsModelMixin.Permission.W)
    serializer = ArticleSerializer
    form_class = FavoriteForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['content_type'] = 'article'
        return kwargs

    def get_serializer_kwargs(self, obj, **kwargs):
        serializer_kwargs = super().get_serializer_kwargs(obj, **kwargs)
        serializer_kwargs['user'] = self.request.user
        return serializer_kwargs

    def post(self, request, *args, **kwargs):
        inst = super().post(request, *args, **kwargs)
        return inst.content_object


class FavoriteDigestDeleteView(SerializerMixin, DeleteView):
    authorized_permission = (PermissionsModelMixin.Permission.R,
                             PermissionsModelMixin.Permission.D)
    model = FavoriteItem
    serializer = DigestSerializer

    class FavoriteForm(forms.Form):
        object_id = forms.IntegerField()

    def get_args_form(self):
        return self.FavoriteForm

    def get_object(self):
        content_type = ContentType.objects.get(model='digest')
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
            return Digest.objects.get(id=self.request_args['object_id'])
        except Digest.DoesNotExist:
            raise ServerError(ServerError.NOT_FOUND)


class FavoriteArticleDeleteView(SerializerMixin, DeleteView):
    authorized_permission = (PermissionsModelMixin.Permission.R,
                             PermissionsModelMixin.Permission.D)
    model = FavoriteItem
    serializer = ArticleSerializer

    class FavoriteForm(forms.Form):
        object_id = forms.IntegerField()

    def get_args_form(self):
        return self.FavoriteForm

    def get_object(self):
        content_type = ContentType.objects.get(model='article')
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
            return Article.objects.get(id=self.request_args['object_id'])
        except Article.DoesNotExist:
            raise ServerError(ServerError.NOT_FOUND)
