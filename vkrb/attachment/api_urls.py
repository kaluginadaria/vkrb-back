from django.urls import path

from vkrb.attachment.views import UploadImageView

app_name = 'attachment'
urlpatterns = [
    path('upload/', UploadImageView.as_view()),

]
