from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from Project_LL.settings import BASE_DIR

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('login.urls')),
    path('dashboard/', include('Indicadores.urls')),
    path('api/', include('Indicadores.api_urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root= settings.STATICFILES_DIRS[0])