from django.urls import path

from vkrb.favorites.views import FavoritesListView

app_name = 'favorites'
urlpatterns = [
    path('get_favorites/', FavoritesListView.as_view()),

]
