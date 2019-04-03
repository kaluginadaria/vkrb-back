from django.urls import path

from vkrb.search.views import SearchView

app_name = 'search'
urlpatterns = [
    path('get/', SearchView.as_view()),
]
