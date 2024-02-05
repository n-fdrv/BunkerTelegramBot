from datetime import datetime

from django.apps import apps

from bot.models import User
from core.config.logging import log_schedulers


async def get_bot_and_scheduler():
    """Метод получения бота и шедулера."""
    app_config = apps.get_app_config("bot")
    app = app_config.bot
    scheduler = app.get_scheduler()
    bot = app.get_bot()
    return bot, scheduler


@log_schedulers
async def send_message_to_all_users(text: str):
    """Шедулер отправки сообщения всем пользователям."""
    bot, scheduler = await get_bot_and_scheduler()
    async for user in User.objects.filter(is_admin=True):
        scheduler.add_job(
            bot.send_message,
            "date",
            run_date=datetime.now(),
            args=[user.telegram_id, text],
        )
