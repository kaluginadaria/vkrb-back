from django import forms
from django.contrib.contenttypes.models import ContentType
from django.db.models import Count
from django_serializer.base_views import (ListView,
                                          DetailsView,
                                          BaseView,
                                          CreateView,
                                          DeleteView)
from django_serializer.exceptions import ServerError
from django_serializer.mixins import ObjectMixin, SerializerMixin, CsrfExemptMixin
from django_serializer.permissions import (
    PermissionsModelMixin,
    PermissionsMixin,
)

from vkrb.core.mixins import EventMixin, LimitOffsetFullPaginator
from vkrb.core.utils import get_absolute_bundle_urls, render_to_pdf
from vkrb.favorites.forms import FavoriteForm
from vkrb.favorites.models import FavoriteItem
from vkrb.newsitem.models import NewsItem, CategoryNewsItem, NewsKeyword
from vkrb.newsitem.serializers import (
    NewsItemSerializer,
    CategoryNewsItemSerializer,
)


class NewsListView(EventMixin, ListView):
    class CategoryForm(forms.Form):
        # category_id = forms.ModelChoiceField(CategoryNewsItem.objects.all(),
        #                                      required=False)
        sort = forms.CharField(required=False)

    def get_serializer_kwargs(self, obj, **kwargs):
        serializer_kwargs = super().get_serializer_kwargs(obj, **kwargs)
        serializer_kwargs['user'] = self.request.user
        return serializer_kwargs

    def get_queryset(self):
        queryset = super().get_queryset().order_by('-created')
        # category = self.request_args.get('category_id')
        sort = self.request_args.get('sort')

        # if category:
        #     return queryset.filter(category=category)

        if sort == 'popular':
            content_type = ContentType.objects.get(model='newsitem')

            sorted_items = FavoriteItem.objects.filter(content_type=content_type).values('object_id').annotate(
                num_favorite=Count('object_id')).order_by('-num_favorite')
            news_list = []
            for item in sorted_items:
                try:
                    news_list.append(NewsItem.objects.get(id=item.get('object_id')))
                except NewsItem.DoesNotExist:
                    continue

            return news_list

        return queryset

    section = 'news'
    args_form = CategoryForm
    authorized_permission = (PermissionsModelMixin.Permission.R,)
    paginator = LimitOffsetFullPaginator
    model = NewsItem
    serializer = NewsItemSerializer


class NewsGetView(DetailsView):
    authorized_permission = (PermissionsModelMixin.Permission.R,)
    model = NewsItem
    serializer = NewsItemSerializer

    def get_serializer_kwargs(self, obj, **kwargs):
        serializer_kwargs = super().get_serializer_kwargs(obj, **kwargs)
        serializer_kwargs['user'] = self.request.user
        return serializer_kwargs


class CategoryView(ListView):
    authorized_permission = (PermissionsModelMixin.Permission.R,)
    model = CategoryNewsItem
    serializer = CategoryNewsItemSerializer
    paginator = LimitOffsetFullPaginator

    def get_queryset(self):
        return self.model.objects.all().order_by('order')


class CreatePDFView(ObjectMixin, PermissionsMixin, BaseView):
    model = NewsItem
    authorized_permission = (PermissionsModelMixin.Permission.R,)

    def response_wrapper(self, response):
        return response

    def get(self, request, *args, **kwargs):
        self.check_r_permission(self.request.user)
        newsitem = self.get_object()
        ctx = {
            'photos': newsitem.attachments.all().order_by('attachments__order'),
            'newsitem': newsitem,
            'css_urls': get_absolute_bundle_urls('pdf', 'css'),
        }
        return render_to_pdf(template_path='newsitem.html', ctx=ctx)


class FavoriteNewsCreateView(CreateView):
    authorized_permission = (PermissionsModelMixin.Permission.R,
                             PermissionsModelMixin.Permission.W)
    serializer = NewsItemSerializer
    form_class = FavoriteForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['content_type'] = 'newsitem'
        return kwargs

    def get_serializer_kwargs(self, obj, **kwargs):
        serializer_kwargs = super().get_serializer_kwargs(obj, **kwargs)
        serializer_kwargs['user'] = self.request.user
        return serializer_kwargs

    def post(self, request, *args, **kwargs):
        inst = super().post(request, *args, **kwargs)
        return inst.content_object


class FavoriteNewsDeleteView(SerializerMixin, DeleteView):
    authorized_permission = (PermissionsModelMixin.Permission.R,
                             PermissionsModelMixin.Permission.D)
    model = FavoriteItem
    serializer = NewsItemSerializer

    class FavoriteForm(forms.Form):
        object_id = forms.IntegerField()

    def get_args_form(self):
        return self.FavoriteForm

    def get_object(self):
        content_type = ContentType.objects.get(model='newsitem')
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
            return NewsItem.objects.get(id=self.request_args['object_id'])
        except NewsItem.DoesNotExist:
            raise ServerError(ServerError.NOT_FOUND)


class DiagramView(CsrfExemptMixin, PermissionsMixin, BaseView):
    def get(self, request, *args, **kwargs):
        self.check_r_permission(self.request.user)
        limit = int(self.request.GET.get('limit'))
        result = []
        queryset = NewsItem.keywords.through.objects.values('newskeyword_id').annotate(
            amount_keys=Count('newskeyword_id')).order_by('-amount_keys')
        k = 0
        for q in queryset:
            try:
                result.append(
                    {
                        'tag': NewsKeyword.objects.get(id=q.get('newskeyword_id')).title,
                        'amount': q.get('amount_keys')
                    }
                )
                k += 1
                if k >= limit:
                    break
            except NewsKeyword.DoesNotExist:
                pass
        return result
