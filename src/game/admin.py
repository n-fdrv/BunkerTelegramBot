from django.contrib import admin

from game.models import ActionCart, Character, Game, InformationCart, Room


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    """Управление моделью пользователя."""

    list_display = (
        "slug",
        "admin",
        "started",
    )
    list_filter = ("started",)
    search_fields = ("slug",)
    readonly_fields = (
        "slug",
        "started",
    )


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


class InformationCharacterInline(admin.TabularInline):
    """Инлайн модель карт информации персонажа."""

    model = Character.information_carts.through
    extra = 1


class ActionCharacterInline(admin.TabularInline):
    """Инлайн модель карт действий персонажа."""

    model = Character.action_carts.through
    extra = 1


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    """Управление персонажами."""

    list_display = ("__str__", "user", "game")
    list_filter = ("user",)
    search_fields = ("user",)
    empty_value_display = "Удален"
    inlines = (InformationCharacterInline, ActionCharacterInline)

    def has_change_permission(self, request, obj=None):
        """Запрещает менять объект."""
        return False


class InformationGameInline(admin.TabularInline):
    """Инлайн модель карт информаций игры."""

    model = Game.information_carts.through
    extra = 1


class UniqueCartsInline(admin.TabularInline):
    """Инлайн модель уникальных карт игры."""

    model = Game.unique_carts.through
    extra = 1


class UserGameInline(admin.TabularInline):
    """Инлайн модель пользователей в игре."""

    model = Game.users.through
    extra = 1


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    """Управление играми."""

    list_display = ("__str__", "created_date", "closed", "closed_date")
    list_filter = ("closed",)
    inlines = (
        UserGameInline,
        InformationGameInline,
    )

    def has_change_permission(self, request, obj=None):
        """Запрещает менять объект."""
        return False
