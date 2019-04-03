from django.urls import path

from vkrb.text.views import TextGetView

app_name = 'text'
urlpatterns = [
    path('get/', TextGetView.as_view()),
]
