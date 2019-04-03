from django.urls import path, include

app_name = 'api'
urlpatterns = [

    path('o.', include('vkrb.oauth.api_urls')),
    path('auth.', include('vkrb.auth.api_urls')),
    path('user.', include('vkrb.user.api_urls')),
    path('news.', include('vkrb.newsitem.api_urls')),
    path('recourse.', include('vkrb.recourse.api_urls')),
    path('expert.', include('vkrb.expert.api_urls')),
    path('text.', include('vkrb.text.api_urls')),
    path('popular.', include('vkrb.popular.api_urls')),
    path('event.', include('vkrb.event.api_urls')),
    path('calc.', include('vkrb.calc.api_urls')),
    path('education.', include('vkrb.education.api_urls')),
    path('activity.', include('vkrb.activity.api_urls')),
    path('digest.', include('vkrb.digest.api_urls')),
    path('matrix.', include('vkrb.matrix.api_urls')),
    path('favorites.', include('vkrb.favorites.api_urls')),
    path('feedback.', include('vkrb.feedback.api_urls')),
    path('attachment.', include('vkrb.attachment.api_urls')),
    path('search.', include('vkrb.search.api_urls')),
]
