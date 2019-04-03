from django.urls import path

from vkrb.activity.views import (GiListView, SiListView,
                                     FavoriteGiCreateView,
                                     FavoriteSiCreateView,
                                     FavoriteGiDeleteView,
                                     FavoriteSiDeleteView,
                                     GiGetView,
                                     SiGetView)

app_name = 'activity'
urlpatterns = [
    path('list_gi/', GiListView.as_view()),
    path('list_si/', SiListView.as_view()),
    path('get_gi/', GiGetView.as_view()),
    path('get_si/', SiGetView.as_view()),
    path('add_favorite_gi/', FavoriteGiCreateView.as_view()),
    path('add_favorite_si/', FavoriteSiCreateView.as_view()),
    path('delete_favorite_gi/', FavoriteGiDeleteView.as_view()),
    path('delete_favorite_si/', FavoriteSiDeleteView.as_view()),

]
