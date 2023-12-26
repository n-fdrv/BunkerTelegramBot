from bot.models import User


def get_user_url(user: User) -> str:
    """Метод формирования ссылки на пользователя."""
    name = user.first_name
    if user.telegram_username:
        name = user.telegram_username
    return f"[{name}](tg://user?id={str(user.telegram_id)})"
