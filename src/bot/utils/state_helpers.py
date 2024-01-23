from bot.models import Character, User


async def get_user(user_id: int) -> User:
    """Метод получения пользователя из базы данных."""
    return await User.objects.select_related(
        "room", "game", "room__admin"
    ).aget(telegram_id=user_id)


async def get_character(user: User) -> Character:
    """Метод получения персонажа из базы данных."""
    return await Character.objects.select_related(
        "game",
        "profession",
        "gender",
        "orientation",
        "health",
        "phobia",
        "hobby",
        "personality",
        "information",
        "item",
        "action_one",
        "action_two",
    ).aget(user=user, game=user.game)
