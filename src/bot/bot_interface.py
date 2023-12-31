import asyncio

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from django.conf import settings
from loguru import logger

from bot.handlers import command_handlers, game_handlers, room_handlers


class AiogramApp:
    """Класс бота."""

    def __init__(self) -> None:
        """Создает бота."""
        self.__TOKEN = settings.TELEGRAM_TOKEN
        self.bot = Bot(token=self.__TOKEN, parse_mode="HTML")
        self.dispatcher = Dispatcher(bot=self.bot)
        self.scheduler = AsyncIOScheduler()
        logger.info("Bot instance created")

    def _download_routes(self, routes):
        """Добавляет роуты боту."""
        head = self.dispatcher
        for route in routes:
            tail = route
            head.include_router(tail)
            head = route

    def start(self) -> None:
        """Запускает бота."""
        routes = [
            command_handlers.router,
            room_handlers.router,
            game_handlers.router,
        ]
        self._download_routes(routes)
        asyncio.ensure_future(
            self.bot.set_my_commands(
                [
                    BotCommand(command="start", description="Запустить бота"),
                    BotCommand(
                        command="new_room",
                        description="Создать комнату для игры",
                    ),
                    BotCommand(
                        command="enter_room", description="Зайти в комнату"
                    ),
                    BotCommand(command="my_room", description="Моя комната"),
                    BotCommand(
                        command="leave_room", description="Выйти из комнаты"
                    ),
                    BotCommand(command="help", description="Помощь"),
                    BotCommand(command="rules", description="Правила Игры"),
                ]
            )
        )
        asyncio.ensure_future(
            self.dispatcher.start_polling(self.bot, skip_updates=True)
        )

        self.scheduler.start()

    def stop(self) -> None:
        """Останавливает бота."""
        asyncio.ensure_future(self.dispatcher.stop_polling())

    def get_bot(self):
        """Метод получения бота."""
        return self.bot

    def get_scheduler(self):
        """Метод получения шедулера."""
        return self.scheduler
