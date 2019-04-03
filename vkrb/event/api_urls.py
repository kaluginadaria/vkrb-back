from django.urls import path

from vkrb.event.views import EventListView, EventTypeListView

app_name = 'event'
urlpatterns = [
    path('list/', EventListView.as_view()),
    path('get_types/', EventTypeListView.as_view()),

]
