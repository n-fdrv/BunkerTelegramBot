from django.contrib import admin

from game.models import ActionCart, InformationCart


@admin.register(InformationCart)
class InformationCartAdmin(admin.ModelAdmin):
    """Управление информационными картами."""

    list_display = (
        "name",
        "type",
    )
    list_display_links = ("name",)
    list_filter = ("type",)
    search_fields = ("name",)


@admin.register(ActionCart)
class ActionCartAdmin(admin.ModelAdmin):
    """Управление картами действия."""

    list_display = ("name", "key", "target", "value")
    list_display_links = ("name",)
    list_filter = ("key", "target", "value")
    search_fields = ("name",)
