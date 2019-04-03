from django.urls import path

from vkrb.recourse.views import (RecourseListView,
                                     RecourseGetView,
                                     RecourseCreateView,
                                     SpecialtyListView,
                                     LikeCreateView,
                                     LikeDeleteView,
                                     CreatePDFView,
                                     FavoriteRecourseCreateView,
                                     FavoriteRecourseDeleteView)

app_name = 'recourse'
urlpatterns = [
    path('list/', RecourseListView.as_view()),
    path('get/', RecourseGetView.as_view()),
    path('create/', RecourseCreateView.as_view()),
    path('get_specialties/', SpecialtyListView.as_view()),
    path('add_like/', LikeCreateView.as_view()),
    path('delete_like/', LikeDeleteView.as_view()),
    path('create_pdf/', CreatePDFView.as_view()),
    path('add_favorite/', FavoriteRecourseCreateView.as_view()),
    path('delete_favorite/', FavoriteRecourseDeleteView.as_view()),

]
