from django.urls import path
from vkrb.education.views import (
    InternalEducationListView,
    CategoryCatalogListView,
    CategoryLibraryListView,
    CatalogItemListView,
    CatalogItemGetView,
    ReductionListView,
    CatalogItemGetPDFView,
    ScienceArticleListView,
    ScienceArticleGetView,
    LiteratureListView,
    ArticleGetPDFView,
    LiteratureItemGetPDFView,
    FavoriteEducationCreateView,
    FavoriteScienceArticleCreateView,
    FavoriteLiteratureCreateView,
    FavoriteCatalogCreateView,
    FavoriteEducationDeleteView,
    FavoriteScienceArticleDeleteView,
    FavoriteCatalogDeleteView,
    FavoriteLiteratureDeleteView)

app_name = 'education'
urlpatterns = [
    path('internal_list/', InternalEducationListView.as_view()),
    path('library_category_list/', CategoryLibraryListView.as_view()),
    path('catalog_category_list/', CategoryCatalogListView.as_view()),
    path('catalog_list/', CatalogItemListView.as_view()),
    path('catalog_get/', CatalogItemGetView.as_view()),
    path('catalog_get_pdf/', CatalogItemGetPDFView.as_view()),
    path('reduction_list/', ReductionListView.as_view()),
    path('science_article_list/', ScienceArticleListView.as_view()),
    path('get_science_article/', ScienceArticleGetView.as_view()),
    path('literature_list/', LiteratureListView.as_view()),
    path('article_get_pdf/', ArticleGetPDFView.as_view()),
    path('literature_get_pdf/', LiteratureItemGetPDFView.as_view()),
    path('add_favorite_internaleducation/', FavoriteEducationCreateView.as_view()),
    path('add_favorite_sciencearticle/', FavoriteScienceArticleCreateView.as_view()),
    path('add_favorite_literature/', FavoriteLiteratureCreateView.as_view()),
    path('add_favorite_catalogitem/', FavoriteCatalogCreateView.as_view()),
    path('delete_favorite_internaleducation/', FavoriteEducationDeleteView.as_view()),
    path('delete_favorite_sciencearticle/', FavoriteScienceArticleDeleteView.as_view()),
    path('delete_favorite_literature/', FavoriteLiteratureDeleteView.as_view()),
    path('delete_favorite_catalogitem/', FavoriteCatalogDeleteView.as_view()),

]
