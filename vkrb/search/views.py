from django import forms
from django_serializer.base_views import ListView
from django_serializer.paginator import LimitOffsetPaginator

from vkrb.search.models import SearchEntity
from vkrb.search.serializers import SearchEntitySerializer


class SearchView(ListView):
    class SearchForm(forms.Form):
        q = forms.CharField(required=True)

    args_form = SearchForm
    model = SearchEntity
    serializer = SearchEntitySerializer

    def get_serializer_kwargs(self, obj, **kwargs):
        serializer_kwargs = super().get_serializer_kwargs(obj, **kwargs)
        serializer_kwargs['user'] = self.request.user
        return serializer_kwargs

    def get_queryset(self):
        return super().get_queryset().filter(
            search_vector=self.request_args['q']
        ).order_by('-id')[:25]
