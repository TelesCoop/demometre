from django.conf import settings
from django.urls import include, path
from django.contrib import admin

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls

from .wagtail_api import api_router


urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("api/cms/", api_router.urls),
    path("api/auth/", include("my_auth.urls", namespace="auth")),
    path("api/", include("open_democracy_back.api_urls")),
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("backup/", include("telescoop_backup.urls")),
    path("hijack/", include("hijack.urls")),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns.append(path("__debug__/", include("debug_toolbar.urls")))
