from django.db import models


class Room(models.Model):
    """Модель для хранения комнат."""

    slug = models.IntegerField(verbose_name="Номер комнаты", unique=True)
    admin = models.ForeignKey(
        to="User",
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


class Cart(models.Model):
    """Модель хранения карточек игры."""

    name = models.CharField(
        max_length=256, verbose_name="Название карточки", unique=True
    )
    type = models.SlugField(max_length=256, verbose_name="Тип карточки")

    class Meta:
        verbose_name = "Карточка"
        verbose_name_plural = "Карточки"

    def __str__(self):
        return f"{self.name}"


class Game(models.Model):
    """Модель для хранения партий игры."""

    epidemia = models.ForeignKey(
        Cart(type="epidemia_cart"),
        on_delete=models.CASCADE,
        verbose_name="Тип катастрофы",
        related_name="epidemia",
    )
    epidemia_time = models.IntegerField(
        verbose_name="Лет до выхода на поверхность"
    )
    bunker_type = models.ForeignKey(
        Cart(type="bunker_type_cart"),
        on_delete=models.CASCADE,
        verbose_name="Тип бункера",
        related_name="bunker_type",
    )
    bunker_place_amount = models.IntegerField(
        verbose_name="Количество мест в бункере"
    )
    room_one = models.ForeignKey(
        Cart(type="room_cart"),
        on_delete=models.CASCADE,
        verbose_name="Комната №1",
        related_name="room_one",
    )
    room_two = models.ForeignKey(
        Cart(type="room_cart"),
        on_delete=models.CASCADE,
        verbose_name="Комната №2",
        related_name="room_two",
    )
    room_three = models.ForeignKey(
        Cart(type="room_cart"),
        on_delete=models.CASCADE,
        verbose_name="Комната №3",
        related_name="room_three",
    )
    is_closed = models.BooleanField(default=False, verbose_name="Сыграна")

    class Meta:
        verbose_name = "Игра"
        verbose_name_plural = "Игры"

    def __str__(self):
        return f"Игра №{self.pk} | Сыграна: {self.is_closed}"


class User(models.Model):
    """Модель для хранения пользователей."""

    telegram_id = models.BigIntegerField(
        verbose_name="Telegram User ID", unique=True
    )
    first_name = models.CharField(
        max_length=255, verbose_name="Имя", null=True, blank=True
    )
    last_name = models.CharField(
        max_length=255, verbose_name="Фамилия", null=True, blank=True
    )
    telegram_username = models.CharField(
        max_length=255,
        verbose_name="Ник в телеграмме",
        null=True,
        blank=True,
    )
    room = models.ForeignKey(
        Room,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Комната",
    )
    game = models.ForeignKey(
        Game,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Игра",
    )
    registration_date = models.DateField(
        auto_now_add=True, verbose_name="Дата регистрации"
    )
    last_login_date = models.DateField(
        auto_now=True, verbose_name="Заходил в последний раз"
    )
    is_admin = models.BooleanField(
        default=False, verbose_name="Права администратора"
    )

    @property
    def full_name(self):
        """Возвращает полное имя пользователя."""
        return f"{self.name} {self.last_name}"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        if self.first_name and self.last_name:
            return (
                f"{self.first_name} {self.last_name} | id: {self.telegram_id}"
            )
        return f"{self.telegram_username} | id: {self.telegram_id}"


class Character(models.Model):
    """Модель для хранения сгенерированных персонажей."""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    age = models.IntegerField(verbose_name="Возраст")
    gender = models.ForeignKey(
        Cart(type="gender_cart"),
        on_delete=models.CASCADE,
        verbose_name="Пол",
        related_name="gender",
    )
    orientation = models.ForeignKey(
        Cart(type="orientation_cart"),
        on_delete=models.CASCADE,
        verbose_name="Ориентация",
        related_name="orientation",
    )
    profession = models.ForeignKey(
        Cart(type="prof_cart"),
        on_delete=models.CASCADE,
        verbose_name="Профессия",
        related_name="profession",
    )
    health = models.ForeignKey(
        Cart(type="health_cart"),
        on_delete=models.CASCADE,
        verbose_name="Здоровье",
        related_name="health",
    )
    phobia = models.ForeignKey(
        Cart(type="phobia_cart"),
        on_delete=models.CASCADE,
        verbose_name="Фобия",
        related_name="phobia",
    )
    personality = models.ForeignKey(
        Cart(type="personality_cart"),
        on_delete=models.CASCADE,
        verbose_name="Характер",
        related_name="personality",
    )
    hobby = models.ForeignKey(
        Cart(type="hobby_cart"),
        on_delete=models.CASCADE,
        verbose_name="Хобби",
        related_name="hobby",
    )
    information = models.ForeignKey(
        Cart(type="ad_info_cart"),
        on_delete=models.CASCADE,
        verbose_name="Дополнительная информация",
        related_name="information",
    )
    item = models.ForeignKey(
        Cart(type="item_cart"),
        on_delete=models.CASCADE,
        verbose_name="Багаж",
        related_name="item",
    )
    action_one = models.ForeignKey(
        Cart(type="action_cart"),
        on_delete=models.CASCADE,
        verbose_name="Карта действий №1",
        related_name="action_one",
    )
    action_two = models.ForeignKey(
        Cart(type="action_cart"),
        on_delete=models.CASCADE,
        verbose_name="Карта действий №2",
        related_name="action_two",
    )
    game = models.ForeignKey(
        Game, on_delete=models.CASCADE, verbose_name="Игра"
    )

    class Meta:
        verbose_name = "Персонаж"
        verbose_name_plural = "Персонажи"

    def __str__(self):
        return (
            f"{self.profession} {self.age} {self.gender} | "
            f"Пользователь: {self.user}"
        )

    def get_main_info(self):
        """Метод получения основной информации о персонаже."""
        return (
            f"{self.profession} - {self.gender} "
            f"{self.age} лет ({self.orientation})"
        )
