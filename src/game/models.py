from django.db import models


class KeyAction(models.TextChoices):
    """Ключ действия."""

    NO_KEY = "no_key", "Нет ключа"
    STEAL = "steal", "Украсть"
    CHANGE = "change", "Изменить"
    TRADE = "trade", "Обмен"
    INFO = "info", "Информация"
    REVEAL = "reveal", "Раскрыть"
    HEAL = "heal", "Вылечить"
    DELETE = "delete", "Удалить"
    INCREASE = "increase", "Увеличить"
    DECREASE = "decrease", "Уменьшить"


class TargetAction(models.TextChoices):
    """Цель действия."""

    NO_TARGET = "no_target", "Нет цели"
    SELF = "self", "Себя"
    ANY = "any", "Любого"
    ALL = "all", "Все"


class ValueAction(models.TextChoices):
    """Переменная действия."""

    NO_VALUE = "no_value", "Нет переменной"
    EPIDEMIA = "epidemia", "Эпидемия"
    BUNKER_TYPE = "bunker_type", "Тип бункера"
    BUNKER_ROOM = "bunker_room", "Комната бункера"
    BUNKER_SUPPLY = "bunker_suply", "Припасы в бункере"
    PROFESSION = "profession", "Профессия"
    AGE = "age", "Возраст"
    GENDER = "gender", "Пол"
    ORIENTATION = "orientation", "Ориентация"
    BIO = "bio", "Био. Характеристики"
    HEALTH = "health", "Здоровье"
    PHOBIA = "phobia", "Фобия"
    PERSONALITY = "personality", "Характер"
    HOBBY = "hobby", "Хобби"
    ADDITIONAL_INFO = "add_info", "Доп. Информация"
    ITEM = "item", "Багаж"
    BUNKER_PLACE = "bunker_place", "Мест в бункере"


class TypeInformationCarts(models.TextChoices):
    """Типы информационных карт."""

    EPIDEMIA = "epidemia", "Эпидемия"
    BUNKER_TYPE = "bunker_type", "Тип бункера"
    BUNKER_ROOM = "bunker_room", "Комната бункера"
    PROFESSION = "profession", "Профессия"
    GENDER = "gender", "Пол"
    ORIENTATION = "orientation", "Ориентация"
    HEALTH = "health", "Здоровье"
    PHOBIA = "phobia", "Фобия"
    PERSONALITY = "personality", "Характер"
    HOBBY = "hobby", "Хобби"
    ADDITIONAL_INFO = "add_info", "Доп. Информация"
    ITEM = "item", "Багаж"


class ActionCart(models.Model):
    """Модель хранения действий персонажа."""

    name = models.CharField(
        max_length=256, verbose_name="Название", unique=True
    )
    key = models.CharField(
        max_length=32,
        choices=KeyAction.choices,
        default=KeyAction.NO_KEY,
        verbose_name="Ключ действия",
    )
    target = models.CharField(
        max_length=32,
        choices=TargetAction.choices,
        default=TargetAction.NO_TARGET,
        verbose_name="Цель действия",
    )
    value = models.CharField(
        max_length=32,
        choices=ValueAction.choices,
        default=ValueAction.NO_VALUE,
        verbose_name="Переменная действия",
    )

    class Meta:
        verbose_name = "Карта Действия"
        verbose_name_plural = "Карты Действия"

    def __str__(self):
        return f"{self.name}"


class InformationCart(models.Model):
    """Модель хранения карт информации."""

    name = models.CharField(
        max_length=256, verbose_name="Название", unique=True
    )
    type = models.CharField(
        max_length=32,
        choices=TypeInformationCarts.choices,
        verbose_name="Тип карты",
    )

    class Meta:
        verbose_name = "Карта Информации"
        verbose_name_plural = "Карты Информации"

    def __str__(self):
        return f"{self.name}"


# class Character(models.Model):
#     """Модель для хранения сгенерированных персонажей."""
#
#     user = models.ForeignKey(
#         User, on_delete=models.CASCADE, verbose_name="Пользователь"
#     )
#     age = models.IntegerField(verbose_name="Возраст")
#     # game = models.ForeignKey(
#     #     Game, on_delete=models.CASCADE, verbose_name="Игра"
#     # )
#
#     class Meta:
#         verbose_name = "Персонаж"
#         verbose_name_plural = "Персонажи"
#
#     def __str__(self):
#         return (
#             f"{self.profession} {self.age} {self.gender} | "
#             f"Пользователь: {self.user}"
#         )
#
#     def get_main_info(self):
#         """Метод получения основной информации о персонаже."""
#         return (
#             f"{self.profession} - {self.gender} "
#             f"{self.age} лет ({self.orientation})"
#         )
