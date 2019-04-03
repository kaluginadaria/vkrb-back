from django.urls import path

from vkrb.calc.views import (
    FormulaListView,
    FormulaGetView,
    FormulaCalcView,
    CreateFormulaPDFView,
    FavoriteFormulaCreateView, FavoriteFormulaDeleteView)

app_name = 'calc'
urlpatterns = [
    path('list/', FormulaListView.as_view()),
    path('get/', FormulaGetView.as_view()),
    path('calc/', FormulaCalcView.as_view()),
    path('create_formula_pdf/', CreateFormulaPDFView.as_view()),
    path('add_favorite/', FavoriteFormulaCreateView.as_view()),
    path('delete_favorite/', FavoriteFormulaDeleteView.as_view()),
]
