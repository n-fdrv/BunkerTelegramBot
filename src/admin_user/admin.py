from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

ADMIN_HEADER = "Администрирование PacanBotTelegram"
ADMIN_TITLE = "Панель администратора бота"

AdminUser = get_user_model()

admin.site.unregister(Group)
admin.site.site_header = ADMIN_HEADER
admin.site.index_title = ADMIN_TITLE


@admin.register(AdminUser)
class AdminUserAdmin(UserAdmin):
    """Управление админкой."""

    pass
