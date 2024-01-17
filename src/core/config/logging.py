import sys

from loguru import logger


def setup_logger():
    """Функция для настройки логгера."""
    logger.remove(0)
    logger.add(
        sys.stdout, level="DEBUG", enqueue=True, backtrace=True, diagnose=True
    )
    logger.add(
        "logs/{time:YYYY-MM-DD}.log",
        rotation="1 month",
        level="INFO",
        enqueue=True,
        backtrace=True,
        diagnose=True,
    )


def log_in_dev(func: object) -> object:
    """Декоратор для логирования обработчиков."""

    async def wrapper(*args, **kwargs):
        message = args[0]
        state = kwargs.get("state")
        callback_data = kwargs.get("callback_data")
        args_data = [state]
        func_type = "Handler"
        if callback_data:
            args_data.append(callback_data)
            func_type = "Callback"
        user = message.from_user if message else None
        user_id = user.id if user else "Unknown"
        username = user.username if user else "Unknown"

        try:
            result = await func(message, *args_data)
            text = (
                f"User: {username} "
                f"(ID: {user_id}) | "
                f"{func_type}: {func.__name__}"
            )
            if callback_data:
                text += f" | Callback Data: {callback_data}"
            logger.info(text)
            return result
        except Exception as e:
            logger.exception(
                f"User: {username} "
                f"(ID: {user_id}) | "
                f"{func_type}: {func.__name__} | "
                f"Exception: {e}"
            )
            raise e

    return wrapper
