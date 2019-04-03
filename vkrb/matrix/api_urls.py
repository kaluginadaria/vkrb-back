from django.urls import path
from vkrb.matrix.views import MatrixItemListView, MatrixItemGetView

app_name = 'matrix'
urlpatterns = [
    path('list/', MatrixItemListView.as_view()),
    path('get/', MatrixItemGetView.as_view())

]
