from django import forms
from django.contrib.contenttypes.models import ContentType
from django_serializer.base_views import (ListView, DetailsView,
                                          CreateView, DeleteView)
from django_serializer.exceptions import ServerError
from django_serializer.mixins import SerializerMixin
from django_serializer.permissions import PermissionsModelMixin

from vkrb.core.mixins import EventMixin, LimitOffsetFullPaginator
from vkrb.core.utils import get_absolute_bundle_urls, render_to_pdf

from vkrb.education.models import (
    InternalEducation,
    CategoryLibrary,
    CategoryCatalog,
    CatalogItem,
    Reduction,
    ScienceArticle, Literature)
from vkrb.education.serializers import (
    InternalEducationSerializer,
    CategoryLibrarySerializer,
    CategoryCatalogSerializer,
    CatalogItemSerializer,
    ReductionSerializer,
    ShortScienceArticleSerializer, ScienceArticleSerializer,
    LiteratureSerializer, ShortCatalogItemSerializer)
from vkrb.favorites.forms import FavoriteForm
from vkrb.favorites.models import FavoriteItem


class InternalEducationListView(EventMixin, ListView):
    section = 'internal_education'
    authorized_permission = (PermissionsModelMixin.Permission.R,)
    paginator = LimitOffsetFullPaginator
    model = InternalEducation
    serializer = InternalEducationSerializer

    def get_serializer_kwargs(self, obj, **kwargs):
        serializer_kwargs = super().get_serializer_kwargs(obj, **kwargs)
        serializer_kwargs['user'] = self.request.user
        return serializer_kwargs

    def get_queryset(self):
        return self.model.objects.all().order_by('type__order', 'id')


class CategoryLibraryListView(EventMixin, ListView):
    section = 'library'
    authorized_permission = (PermissionsModelMixin.Permission.R,)
    paginator = LimitOffsetFullPaginator
    model = CategoryLibrary
    serializer = CategoryLibrarySerializer

    def get_queryset(self):
        return self.model.objects.all().order_by('order')


class CategoryCatalogListView(ListView):
    class CategoryLibraryForm(forms.Form):
        library = forms.ModelChoiceField(CategoryLibrary.objects.all(), required=True)

    authorized_permission = (PermissionsModelMixin.Permission.R,)
    paginator = LimitOffsetFullPaginator
    model = CategoryCatalog
    serializer = CategoryCatalogSerializer
    args_form = CategoryLibraryForm

    def get_queryset(self):
        queryset = super().get_queryset()
        library = self.request_args.get('library')
        return queryset.filter(library=library).order_by('order')


class CatalogItemListView(ListView):
    class CategoryCatalogForm(forms.Form):
        type = forms.ModelChoiceField(CategoryCatalog.objects.all(), required=True)

    authorized_permission = (PermissionsModelMixin.Permission.R,)
    paginator = LimitOffsetFullPaginator
    model = CatalogItem
    serializer = ShortCatalogItemSerializer
    args_form = CategoryCatalogForm

    def get_serializer_kwargs(self, obj, **kwargs):
        serializer_kwargs = super().get_serializer_kwargs(obj, **kwargs)
        serializer_kwargs['user'] = self.request.user
        return serializer_kwargs

    def get_queryset(self):
        queryset = super().get_queryset()
        type = self.request_args.get('type')
        return queryset.filter(type=type).order_by('order')


class CatalogItemGetView(DetailsView):
    authorized_permission = (PermissionsModelMixin.Permission.R,)
    model = CatalogItem
    serializer = CatalogItemSerializer

    def get_serializer_kwargs(self, obj, **kwargs):
        serializer_kwargs = super().get_serializer_kwargs(obj, **kwargs)
        serializer_kwargs['user'] = self.request.user
        return serializer_kwargs


class CatalogItemGetPDFView(DetailsView):
    authorized_permission = (PermissionsModelMixin.Permission.R,)
    model = CatalogItem

    def response_wrapper(self, response):
        return response

    def get(self, *args, **kwargs):
        ctx = {
            'object': self.get_object(),
            'css_urls': get_absolute_bundle_urls('pdf', 'css'),
        }
        return render_to_pdf(template_path='catalog_item.html', ctx=ctx)


class ReductionListView(ListView):
    class ReductionForm(forms.Form):
        library = forms.ModelChoiceField(CategoryLibrary.objects.all(), required=True)

    authorized_permission = (PermissionsModelMixin.Permission.R,)
    paginator = LimitOffsetFullPaginator
    model = Reduction
    serializer = ReductionSerializer
    args_form = ReductionForm

    def get_queryset(self):
        queryset = super().get_queryset()
        library = self.request_args.get('library')
        return queryset.filter(library=library).order_by('order')


class ScienceArticleListView(ListView):
    class ScienceArticleListForm(forms.Form):
        library = forms.ModelChoiceField(CategoryLibrary.objects.all(),
                                         required=False)

    args_form = ScienceArticleListForm
    authorized_permission = (PermissionsModelMixin.Permission.R,)
    unauthorized_permission = (PermissionsModelMixin.Permission.R,)
    paginator = LimitOffsetFullPaginator
    model = ScienceArticle
    serializer = ShortScienceArticleSerializer

    def get_serializer_kwargs(self, obj, **kwargs):
        serializer_kwargs = super().get_serializer_kwargs(obj, **kwargs)
        serializer_kwargs['user'] = self.request.user
        return serializer_kwargs

    def get_queryset(self):
        queryset = super().get_queryset()
        library = self.request_args.get('library')

        if library:
            queryset = queryset.filter(library=library)

        return queryset


class ScienceArticleGetView(DetailsView):
    authorized_permission = (PermissionsModelMixin.Permission.R,)
    unauthorized_permission = (PermissionsModelMixin.Permission.R,)
    model = ScienceArticle
    serializer = ScienceArticleSerializer

    def get_serializer_kwargs(self, obj, **kwargs):
        serializer_kwargs = super().get_serializer_kwargs(obj, **kwargs)
        serializer_kwargs['user'] = self.request.user
        return serializer_kwargs


class LiteratureListView(ListView):
    class LiteratureListForm(forms.Form):
        library = forms.ModelChoiceField(CategoryLibrary.objects.all(),
                                         required=False)

    args_form = LiteratureListForm
    authorized_permission = (PermissionsModelMixin.Permission.R,)
    unauthorized_permission = (PermissionsModelMixin.Permission.R,)
    paginator = LimitOffsetFullPaginator
    model = Literature
    serializer = LiteratureSerializer

    def get_serializer_kwargs(self, obj, **kwargs):
        serializer_kwargs = super().get_serializer_kwargs(obj, **kwargs)
        serializer_kwargs['user'] = self.request.user
        return serializer_kwargs

    def get_queryset(self):
        queryset = super().get_queryset()
        library = self.request_args.get('library')

        if library:
            queryset = queryset.filter(library=library)

        return queryset


class ArticleGetPDFView(DetailsView):
    authorized_permission = (PermissionsModelMixin.Permission.R,)
    unauthorized_permission = (PermissionsModelMixin.Permission.R,)
    model = ScienceArticle

    def response_wrapper(self, response):
        return response

    def get(self, *args, **kwargs):
        article = self.get_object()
        ctx = {
            'article': article,
            'css_urls': get_absolute_bundle_urls('pdf', 'css'),
        }
        return render_to_pdf(template_path='science_article.html', ctx=ctx)


class LiteratureItemGetPDFView(DetailsView):
    authorized_permission = (PermissionsModelMixin.Permission.R,)
    unauthorized_permission = (PermissionsModelMixin.Permission.R,)
    model = Literature

    def response_wrapper(self, response):
        return response

    def get(self, *args, **kwargs):
        ctx = {
            'literature': self.get_object(),
            'css_urls': get_absolute_bundle_urls('pdf', 'css'),
        }
        return render_to_pdf(template_path='literature.html', ctx=ctx)


class FavoriteLiteratureCreateView(CreateView):
    authorized_permission = (PermissionsModelMixin.Permission.R,
                             PermissionsModelMixin.Permission.W)
    serializer = LiteratureSerializer
    form_class = FavoriteForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['content_type'] = 'literature'
        return kwargs

    def get_serializer_kwargs(self, obj, **kwargs):
        serializer_kwargs = super().get_serializer_kwargs(obj, **kwargs)
        serializer_kwargs['user'] = self.request.user
        return serializer_kwargs

    def post(self, request, *args, **kwargs):
        inst = super().post(request, *args, **kwargs)
        return inst.content_object



class FavoriteEducationCreateView(CreateView):
    authorized_permission = (PermissionsModelMixin.Permission.R,
                             PermissionsModelMixin.Permission.W)
    serializer = InternalEducationSerializer
    form_class = FavoriteForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['content_type'] = 'internaleducation'
        return kwargs

    def get_serializer_kwargs(self, obj, **kwargs):
        serializer_kwargs = super().get_serializer_kwargs(obj, **kwargs)
        serializer_kwargs['user'] = self.request.user
        return serializer_kwargs

    def post(self, request, *args, **kwargs):
        inst = super().post(request, *args, **kwargs)
        return inst.content_object



class FavoriteScienceArticleCreateView(CreateView):
    authorized_permission = (PermissionsModelMixin.Permission.R,
                             PermissionsModelMixin.Permission.W)
    serializer = ScienceArticleSerializer
    form_class = FavoriteForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['content_type'] = 'sciencearticle'
        return kwargs

    def get_serializer_kwargs(self, obj, **kwargs):
        serializer_kwargs = super().get_serializer_kwargs(obj, **kwargs)
        serializer_kwargs['user'] = self.request.user
        return serializer_kwargs

    def post(self, request, *args, **kwargs):
        inst = super().post(request, *args, **kwargs)
        return inst.content_object



class FavoriteCatalogCreateView(CreateView):
    authorized_permission = (PermissionsModelMixin.Permission.R,
                             PermissionsModelMixin.Permission.W)
    serializer = ShortCatalogItemSerializer
    form_class = FavoriteForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['content_type'] = 'catalogitem'
        return kwargs

    def get_serializer_kwargs(self, obj, **kwargs):
        serializer_kwargs = super().get_serializer_kwargs(obj, **kwargs)
        serializer_kwargs['user'] = self.request.user
        return serializer_kwargs

    def post(self, request, *args, **kwargs):
        inst = super().post(request, *args, **kwargs)
        return inst.content_object



class FavoriteEducationDeleteView(SerializerMixin, DeleteView):
    authorized_permission = (PermissionsModelMixin.Permission.R,
                             PermissionsModelMixin.Permission.D)
    model = FavoriteItem
    serializer = InternalEducationSerializer

    class FavoriteForm(forms.Form):
        object_id = forms.IntegerField()

    def get_args_form(self):
        return self.FavoriteForm

    def get_object(self):
        content_type = ContentType.objects.get(model='internaleducation')
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
            return InternalEducation.objects.get(id=self.request_args['object_id'])
        except InternalEducation.DoesNotExist:
            raise ServerError(ServerError.NOT_FOUND)


class FavoriteScienceArticleDeleteView(SerializerMixin, DeleteView):
    authorized_permission = (PermissionsModelMixin.Permission.R,
                             PermissionsModelMixin.Permission.D)
    model = FavoriteItem
    serializer = ScienceArticleSerializer

    class FavoriteForm(forms.Form):
        object_id = forms.IntegerField()

    def get_args_form(self):
        return self.FavoriteForm

    def get_object(self):
        content_type = ContentType.objects.get(model='sciencearticle')
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
            return ScienceArticle.objects.get(id=self.request_args['object_id'])
        except ScienceArticle.DoesNotExist:
            raise ServerError(ServerError.NOT_FOUND)


class FavoriteLiteratureDeleteView(SerializerMixin, DeleteView):
    authorized_permission = (PermissionsModelMixin.Permission.R,
                             PermissionsModelMixin.Permission.D)
    model = FavoriteItem
    serializer = LiteratureSerializer

    class FavoriteForm(forms.Form):
        object_id = forms.IntegerField()

    def get_args_form(self):
        return self.FavoriteForm

    def get_object(self):
        content_type = ContentType.objects.get(model='literature')
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
            return Literature.objects.get(id=self.request_args['object_id'])
        except Literature.DoesNotExist:
            raise ServerError(ServerError.NOT_FOUND)


class FavoriteCatalogDeleteView(SerializerMixin, DeleteView):
    authorized_permission = (PermissionsModelMixin.Permission.R,
                             PermissionsModelMixin.Permission.D)
    model = FavoriteItem
    serializer = ShortCatalogItemSerializer

    class FavoriteForm(forms.Form):
        object_id = forms.IntegerField()

    def get_args_form(self):
        return self.FavoriteForm

    def get_object(self):
        content_type = ContentType.objects.get(model='catalogitem')
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
            return CatalogItem.objects.get(id=self.request_args['object_id'])
        except CatalogItem.DoesNotExist:
            raise ServerError(ServerError.NOT_FOUND)
