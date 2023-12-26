import csv

from django.contrib import admin
from django_object_actions import DjangoObjectActions

from bot.models import Cart, Character, Game, Room, User


@admin.register(User)
class UserAdmin(DjangoObjectActions, admin.ModelAdmin):
    """Управление моделью пользователя."""

    def download_csv(modeladmin, request, queryset):
        """Сформировать файл с данными базы."""
        with open(
            "data/users.csv", "w", newline="", encoding="utf-8"
        ) as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=",")
            for row in queryset:
                spamwriter.writerow(
                    [
                        row.telegram_id,
                        row.first_name,
                        row.last_name,
                        row.telegram_username,
                        row.room,
                        row.registration_date,
                        row.last_login_date,
                    ]
                )

    download_csv.short_description = "Download selected as csv"

    changelist_actions = ("download_csv",)

    list_display = (
        "telegram_id",
        "first_name",
        "last_name",
        "telegram_username",
        "room",
        "registration_date",
        "last_login_date",
    )
    list_filter = ("room",)
    search_fields = ("telegram_id", "telegram_username")
    # readonly_fields = (
    #     "telegram_id",
    #     "room",
    # )


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


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    """Управление моделью карточек игры."""

    list_display = ("name", "type")
    list_filter = ("type",)
    search_fields = ("name",)


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    """Управление моделью сгенерированных персонажей."""

    list_display = (
        "user",
        "room",
        "get_main_info",
    )
    list_filter = ("room", "user")


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    """Управление моделью партий игры."""

    list_display = (
        "room",
        "bunker_type",
        "epidemia",
        "room_one",
        "room_two",
        "room_three",
        "is_closed",
    )
    list_filter = ("is_closed",)
