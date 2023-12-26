from bot.models import User


def get_user_url(user: User) -> str:
    """Метод формирования ссылки на пользователя."""
    name = user.telegram_username
    if user.first_name:
        name = user.first_name
    if user.last_name:
        name += f" {user.last_name}"
    return f"[{name}](tg://user?id={str(user.telegram_id)})"
