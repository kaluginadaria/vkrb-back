import oauth2_provider.views as oauth2_views
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.conf import settings

oauth2_urlpatterns = []

if settings.DEBUG:
    oauth2_urlpatterns += [
        path('applications/', oauth2_views.ApplicationList.as_view(),
             name="list"),
        path('applications/register/',
             oauth2_views.ApplicationRegistration.as_view(), name="register"),
        path('applications/<int:pk>/', oauth2_views.ApplicationDetail.as_view(),
             name="detail"),
        path('applications/<int:pk>/delete/',
             oauth2_views.ApplicationDelete.as_view(), name="delete"),
        path('applications/<int:pk>/update/',
             oauth2_views.ApplicationUpdate.as_view(), name="update"),
    ]
    oauth2_urlpatterns += [
        path('authorized-tokens/',
             oauth2_views.AuthorizedTokensListView.as_view(),
             name="authorized-token-list"),
        path('authorized-tokens/<int:pk>/delete/',
             oauth2_views.AuthorizedTokenDeleteView.as_view(),
             name="authorized-token-delete"),
    ]

oauth2_urlpatterns = (oauth2_urlpatterns, 'oauth2_provider')
urlpatterns = [
    path('jet/', include('jet.urls', 'jet')),
    path('o/', include(oauth2_urlpatterns)),
    path('admin/', admin.site.urls),
    path('api/', include('vkrb.application.api_urls')),
    re_path(r'^chaining/', include('smart_selects.urls')),
]

if settings.DEBUG:
    from revproxy.views import ProxyView


    class AssetsProxyView(ProxyView):
        upstream = settings.PROXY_BASE_URL


    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += [
        re_path(r'assets/bundles/(?P<path>.*)$', AssetsProxyView.as_view()),
    ]
