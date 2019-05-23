from django.urls import path
from vkrb.newsitem.views import NewsListView, NewsGetView, CategoryView, CreatePDFView, FavoriteNewsCreateView, \
    FavoriteNewsDeleteView, DiagramView

app_name = 'newsitem'
urlpatterns = [
    path('list/', NewsListView.as_view()),
    path('get/', NewsGetView.as_view()),
    path('get_categories/', CategoryView.as_view()),
    path('create_pdf/', CreatePDFView.as_view()),
    path('add_favorite/', FavoriteNewsCreateView.as_view()),
    path('delete_favorite/', FavoriteNewsDeleteView.as_view()),
    path('diagram/', DiagramView.as_view()),
]
