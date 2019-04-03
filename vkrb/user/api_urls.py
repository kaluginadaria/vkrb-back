from django.urls import path

from vkrb.user.views import UserView, UserUpdateView, UserUpdatePermsView

app_name = 'user'
urlpatterns = [
    path('get/', UserView.as_view()),
    path('update/', UserUpdateView.as_view()),
    path('check_perm_update/', UserUpdatePermsView.as_view()),
]
