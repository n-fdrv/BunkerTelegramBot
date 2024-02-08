from django.db import models


class KeyAction(models.TextChoices):
    """Ключ действия."""

    NO_KEY = "no_key", "Нет ключа"
    STEAL = "steal", "Украсть"
    CHANGE = "change", "Изменить"
    GENERATE = "generate", "Сгенерировать"
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


class Room(models.Model):
    """Модель для хранения комнат."""

    slug = models.IntegerField(verbose_name="Номер комнаты", unique=True)
    admin = models.ForeignKey(
        to="bot.User",
        on_delete=models.CASCADE,
        verbose_name="Администратор комнаты",
        related_name="room_admin",
        blank=True,
        null=True,
    )
    started = models.BooleanField(verbose_name="Игра начата", default=False)

    class Meta:
        verbose_name = "Комната"
        verbose_name_plural = "Комнаты"

    def __str__(self):
        return f"{self.slug}"


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


class Game(models.Model):
    """Модель для хранения партий игры."""

    epidemia_time = models.IntegerField(
        verbose_name="Лет до выхода на поверхность"
    )
    bunker_place_amount = models.IntegerField(
        verbose_name="Количество мест в бункере"
    )
    information_carts = models.ManyToManyField(
        InformationCart,
        through="InformationGame",
        related_name="information_carts",
    )
    unique_carts = models.ManyToManyField(
        InformationCart, through="UniqueCartGame", related_name="unique_carts"
    )
    users = models.ManyToManyField(
        to="bot.User", through="UserGame", related_name="users"
    )
    created_date = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата начала игры"
    )
    closed = models.BooleanField(default=False, verbose_name="Сыграна")
    closed_date = models.DateTimeField(
        verbose_name="Дата окончания игры", null=True, blank=True
    )

    class Meta:
        verbose_name = "Игра"
        verbose_name_plural = "Игры"

    def __str__(self):
        return f"Игра №{self.pk}"


class UserGame(models.Model):
    """Модель хранения пользователей в играх."""

    user = models.ForeignKey(
        to="bot.User",
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
    )
    game = models.ForeignKey(
        Game, on_delete=models.CASCADE, verbose_name="Игра"
    )

    class Meta:
        verbose_name = "Пользователь в игре"
        verbose_name_plural = "Пользователи в игре"

    def __str__(self):
        return f"{self.user.full_name}"


class InformationGame(models.Model):
    """Модель хранения карточек действий персонажей."""

    cart = models.ForeignKey(
        InformationCart,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Карточка",
    )
    game = models.ForeignKey(
        Game, on_delete=models.CASCADE, verbose_name="Игра"
    )

    class Meta:
        verbose_name = "Карточка информации игры"
        verbose_name_plural = "Карточки информации игры"

    def __str__(self):
        return f"{self.cart}"


class UniqueCartGame(models.Model):
    """Модель хранения уникальных карт в игре."""

    cart = models.ForeignKey(
        InformationCart,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Карточка",
    )
    game = models.ForeignKey(
        Game, on_delete=models.CASCADE, verbose_name="Игра"
    )

    class Meta:
        verbose_name = "Уникальная карта в игре"
        verbose_name_plural = "Уникальные карты в игре"

    def __str__(self):
        return f"{self.cart}"


class Character(models.Model):
    """Модель для хранения сгенерированных персонажей."""

    user = models.ForeignKey(
        to="bot.User",
        on_delete=models.SET_NULL,
        verbose_name="Пользователь",
        null=True,
        blank=True,
    )
    age = models.IntegerField(verbose_name="Возраст")
    information_carts = models.ManyToManyField(
        InformationCart, through="InformationCharacter"
    )
    action_carts = models.ManyToManyField(
        ActionCart, through="ActionCharacter"
    )
    game = models.ForeignKey(
        Game, on_delete=models.CASCADE, verbose_name="Игра"
    )

    class Meta:
        verbose_name = "Персонаж"
        verbose_name_plural = "Персонажи"

    def __str__(self):
        gender = self.information_carts.filter(
            type=TypeInformationCarts.GENDER
        ).last()
        profession = self.information_carts.filter(
            type=TypeInformationCarts.PROFESSION
        ).last()
        return f"{gender} {self.age} лет ({profession})"


class InformationCharacter(models.Model):
    """Модель хранения информационных карточек персонажей."""

    cart = models.ForeignKey(
        InformationCart,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Карточка",
    )
    character = models.ForeignKey(
        Character, on_delete=models.CASCADE, verbose_name="Персонаж"
    )

    class Meta:
        verbose_name = "Карточка информации персонажа"
        verbose_name_plural = "Карточки информации персонажа"

    def __str__(self):
        return f"{self.character.user} | {self.cart.name}"


class ActionCharacter(models.Model):
    """Модель хранения карточек действий персонажей."""

    cart = models.ForeignKey(
        ActionCart,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Карточка",
    )
    character = models.ForeignKey(
        Character, on_delete=models.CASCADE, verbose_name="Персонаж"
    )

    class Meta:
        verbose_name = "Карточка действий персонажа"
        verbose_name_plural = "Карточки действий персонажа"

    def __str__(self):
        return f"{self.character.user} | {self.cart.name}"
