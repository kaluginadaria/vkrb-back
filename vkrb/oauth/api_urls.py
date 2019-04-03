from django.urls import path

from vkrb.oauth.views import TokenView, RevokeTokenView

app_name = 'oauth'
urlpatterns = [
    path('token/', TokenView.as_view()),
    path('revoke-token/', RevokeTokenView.as_view()),
]
