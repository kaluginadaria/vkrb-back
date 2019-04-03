from django.urls import path

from vkrb.auth.views import RegisterView, ActivateView, \
    SaveTokenView, NewPasswordView, ResetPasswordView

app_name = 'auth'
urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('activate/', ActivateView.as_view()),
    path('reset_password/', ResetPasswordView.as_view()),
    path('new_password/', NewPasswordView.as_view()),
    path('save_token/', SaveTokenView.as_view()),
]
