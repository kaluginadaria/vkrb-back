from django import forms
from django import forms
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.forms import FloatField, CharField
import math
from vkrb.calc.models import Formula
from vkrb.calc.utils import FORMULAS, CALC
from vkrb.core.utils import to_int
from vkrb.favorites.models import FavoriteItem


class FormulaCalcForm(forms.ModelForm):
    class Meta:
        model = Formula
        fields = ()

    def full_clean(self):
        self.fields = self.prepare_fields(self.fields)
        super().full_clean()

    def prepare_fields(self, fields):
        formula_fields = FORMULAS.get(self.instance.key, {}).get('input')
        if formula_fields is None:
            raise ValidationError('Такой формулы нет')
        for f in formula_fields:
            name = f['name']
            if name in ['nkt']:
                formtype = CharField(max_length=255, required=True)
            else:
                formtype = FloatField(required=True)
            fields[name] = formtype

        return fields

    def clean_nkt(self):
        nkt = self.cleaned_data.get('nkt')
        params = nkt.split('x')
        if len(params) == 2:
            self.cleaned_data['D'] = to_int(params[0], 0)
            self.cleaned_data['H'] = to_int(params[1], 0)
        else:
            raise ValidationError('Невалидный тип НКТ')
        return nkt

    def clean(self):
        result = {}
        super().clean()
        instance = self.instance
        key = instance.key
        formula = FORMULAS.get(key)
        input = formula.get('input')
        for i in input:
            if i.get('name') not in self.cleaned_data:
                raise ValidationError('Заполните все поля')
        output = formula.get('output')
        params = self.cleaned_data
        constans = formula.get('constant')
        if constans:
            for f in constans:
                params[f.get('name')] = f.get('value')
        for out in output:
            try:
                result[out.get('name')] = round(eval(CALC.get(out.get('formula'))), 2)
            except ValueError:
                raise ValidationError('Некорректные данные')
            except ZeroDivisionError:
                raise ValidationError('Деление на 0')
        self.cleaned_data['result'] = result

        return self.cleaned_data

    def save(self, commit=True):
        instance = super().save(commit)
        result = self.cleaned_data.get('result')
        return result
