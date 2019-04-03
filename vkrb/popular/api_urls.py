from django.urls import path

from vkrb.popular.views import PopularListView

app_name = 'popular'
urlpatterns = [
    path('list/', PopularListView.as_view()),
]
