from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from dddoski import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cms/', include(wagtailadmin_urls)),  # Панель управления Wagtail
    path('documents/', include(wagtaildocs_urls)),
    path('shop/', include('shop.urls')),        # URL-ы приложения магазина
    path('', include(wagtail_urls)),             # Wagtail страницы (главная и др.)
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    pass
