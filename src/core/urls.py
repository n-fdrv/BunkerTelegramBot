from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import user_passes_test
from django.urls import path

from core.views import show_admin_log_file, show_admin_logs

urlpatterns = [
    path(
        "admin/logs/",
        user_passes_test(lambda u: u.is_superuser)(show_admin_logs),
        name="show_admin_logs",
    ),
    path(
        "admin/logs/<str:log_name>/",
        user_passes_test(lambda u: u.is_superuser)(show_admin_log_file),
        name="show_admin_log_file",
    ),
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT,
    )
