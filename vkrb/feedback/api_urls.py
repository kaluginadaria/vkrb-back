from django.urls import path

from vkrb.feedback.views import FeedbackSendView, CategoryFeedbackListView

app_name = 'feedback'
urlpatterns = [
    path('create/', FeedbackSendView.as_view()),
    path('list_category/', CategoryFeedbackListView.as_view()),

]
