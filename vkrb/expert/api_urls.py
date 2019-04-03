from django.urls import path

from vkrb.expert.views import (ExpertListView,
                                   FavoriteExpertCreateView,
                                   FavoriteExpertDeleteView)

app_name = 'expert'
urlpatterns = [
    path('list/', ExpertListView.as_view()),
    path('add_favorite/', FavoriteExpertCreateView.as_view()),
    path('delete_favorite/', FavoriteExpertDeleteView.as_view()),
]
