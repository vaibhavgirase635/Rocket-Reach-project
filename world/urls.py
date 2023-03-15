from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from space.views import LoginAPI
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LoginAPI.as_view(), name="login"),
    path('space/', include('space.urls')),
    path('space2/', include('space2.urls')),
    path('auth/',include('rest_framework.urls',namespace='rest_framework'))
]  
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()