import csv

from django.core.management.base import BaseCommand
from loguru import logger

from game.models import ActionCart


class Command(BaseCommand):
    """Команда заполнения баззы данных."""

    help = "Заполняет базу данных записями"

    def handle(self, *args, **kwargs):
        """Метод при вызове команды."""
        with open("data/actions_carts.csv", encoding="utf-8") as f:
            logger.info("ActionCart upload started")
            reader = csv.reader(f)
            for row in reader:
                try:
                    ActionCart.objects.get_or_create(
                        name=row[0], key=row[1], target=row[2], value=row[3]
                    )
                except Exception as e:
                    logger.error(
                        f"error in uploading: ActionCart - {row[0]}: {e}"
                    )
            logger.info("ActionCart upload ended")
