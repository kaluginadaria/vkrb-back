from django.urls import path

from vkrb.digest.views import (
    DigestCategoryListView,
    DigestListView,
    ArticleListView,
    ArticleGetView,
    CreatePDFView,
    FavoriteArticleCreateView,
    FavoriteDigestCreateView,
    FavoriteArticleDeleteView,
    FavoriteDigestDeleteView)

app_name = 'digest'
urlpatterns = [
    path('category_list/', DigestCategoryListView.as_view()),
    path('list/', DigestListView.as_view()),
    path('article_list/', ArticleListView.as_view()),
    path('get_article/', ArticleGetView.as_view()),
    path('create_pdf/', CreatePDFView.as_view()),
    path('add_favorite_article/', FavoriteArticleCreateView.as_view()),
    path('add_favorite_digest/', FavoriteDigestCreateView.as_view()),
    path('delete_favorite_article/', FavoriteArticleDeleteView.as_view()),
    path('delete_favorite_digest/', FavoriteDigestDeleteView.as_view()),
]
