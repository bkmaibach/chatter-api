from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from .views import api_root


admin.site.site_title = settings.ADMIN_TITLE
admin.site.site_header = settings.ADMIN_HEADER


urlpatterns = [
    # Admin
    url(r'^admin/', admin.site.urls),

    # App routes
    url(r'^', include('apps.file.urls')),
    url(r'^', include('apps.socialmedia.urls')),
    url(r'^', include('apps.user.urls')),

    # Routes for chatter app
    path('chat/', include('chatter.urls')),

    # Browsable API
    url(r'^api/$', api_root, name='index'),
    url(r'^api-auth/', include('rest_framework.urls')),
]

if settings.ENV == settings.DEV:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
