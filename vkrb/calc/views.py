from copy import deepcopy

from django import forms
from django.contrib.contenttypes.models import ContentType
from django_serializer.base_views import (ListView, DetailsView,
                                          CreateView, DeleteView)
from django_serializer.exceptions import ServerError, FormException
from django_serializer.mixins import SerializerMixin
from django_serializer.permissions import PermissionsModelMixin

from vkrb.calc.forms import FormulaCalcForm
from vkrb.calc.models import Formula
from vkrb.calc.serializers import FormulaSerializer
from vkrb.calc.utils import FORMULAS
from vkrb.core.mixins import EventMixin, LimitOffsetFullPaginator
from vkrb.core.utils import render_to_pdf, get_absolute_bundle_urls
from vkrb.favorites.forms import FavoriteForm
from vkrb.favorites.models import FavoriteItem


class FormulaListView(EventMixin, ListView):
    section = 'calc'
    authorized_permission = (PermissionsModelMixin.Permission.R,)
    paginator = LimitOffsetFullPaginator
    model = Formula
    serializer = FormulaSerializer

    def get_serializer_kwargs(self, obj, **kwargs):
        serializer_kwargs = super().get_serializer_kwargs(obj, **kwargs)
        serializer_kwargs['user'] = self.request.user
        return serializer_kwargs

    def get_queryset(self):
        return self.model.objects.all().order_by('order')


class FormulaGetView(DetailsView):
    authorized_permission = (PermissionsModelMixin.Permission.R,)
    model = Formula
    serializer = FormulaSerializer

    def get_serializer_kwargs(self, obj, **kwargs):
        serializer_kwargs = super().get_serializer_kwargs(obj, **kwargs)
        serializer_kwargs['user'] = self.request.user
        return serializer_kwargs


class FormulaCalcView(DetailsView):
    authorized_permission = (PermissionsModelMixin.Permission.R,
                             PermissionsModelMixin.Permission.W)
    model = Formula
    serializer = FormulaSerializer
    form_class = FormulaCalcForm

    def get_serializer_kwargs(self, obj, **kwargs):
        serializer_kwargs = super().get_serializer_kwargs(obj, **kwargs)
        serializer_kwargs['user'] = self.request.user
        return serializer_kwargs

    def get(self, *args, **kwargs):
        raise ServerError(ServerError.NOT_IMPLEMENTED)

    def response_middleware(self, response):
        return response

    def post(self, request, *args, **kwargs):
        self.check_w_permission(self.request.user)
        form = self.get_form()
        if form.is_valid():
            result = form.save()
        else:
            raise FormException(form)
        return result


class CreateFormulaPDFView(DetailsView):
    authorized_permission = (PermissionsModelMixin.Permission.R,
                             PermissionsModelMixin.Permission.W)
    model = Formula
    form_class = FormulaCalcForm

    def post(self, *args, **kwargs):
        raise ServerError(ServerError.NOT_IMPLEMENTED)

    def response_wrapper(self, response):
        return response

    def get(self, request, *args, **kwargs):
        self.check_w_permission(self.request.user)
        form = self.get_form()
        cleaned_data = {}
        if form.is_valid():
            form.save()
            cleaned_data = form.cleaned_data

        formula = self.get_object()
        formula_data = deepcopy(FORMULAS.get(formula.key))

        for item in formula_data['input']:
            k = item['name']
            item['value'] = cleaned_data.get(k)
        if 'result' in cleaned_data:
            result = cleaned_data['result']
            for item in formula_data['output']:
                k = item['name']
                item['value'] = result[k]

        ctx = {
            'formula': formula,
            'formula_data': formula_data,
            'css_urls': get_absolute_bundle_urls('pdf', 'css'),
        }

        return render_to_pdf(template_path='formula.html', ctx=ctx)


class FavoriteFormulaCreateView(CreateView):
    authorized_permission = (PermissionsModelMixin.Permission.R,
                             PermissionsModelMixin.Permission.W)
    serializer = FormulaSerializer
    form_class = FavoriteForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['content_type'] = 'formula'
        return kwargs

    def get_serializer_kwargs(self, obj, **kwargs):
        serializer_kwargs = super().get_serializer_kwargs(obj, **kwargs)
        serializer_kwargs['user'] = self.request.user
        return serializer_kwargs

    def post(self, request, *args, **kwargs):
        inst = super().post(request, *args, **kwargs)
        return inst.content_object



class FavoriteFormulaDeleteView(SerializerMixin, DeleteView):
    authorized_permission = (PermissionsModelMixin.Permission.R,
                             PermissionsModelMixin.Permission.D)
    model = FavoriteItem
    serializer = FormulaSerializer

    class FavoriteForm(forms.Form):
        object_id = forms.IntegerField()

    def get_args_form(self):
        return self.FavoriteForm

    def get_object(self):
        content_type = ContentType.objects.get(model='formula')
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
            return Formula.objects.get(id=self.request_args['object_id'])
        except Formula.DoesNotExist:
            raise ServerError(ServerError.NOT_FOUND)
