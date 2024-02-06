import csv
import os

from django.core.management.base import BaseCommand
from loguru import logger

from game.models import InformationCart


class Command(BaseCommand):
    """Команда заполнения баззы данных."""

    help = "Заполняет базу данных записями"

    def handle(self, *args, **kwargs):
        """Метод при вызове команды."""
        directory = "data/information_carts/"
        files = os.listdir(directory)
        for file in files:
            with open(f"{directory}{file}", encoding="utf-8") as f:
                logger.info(f"{file} upload started")
                reader = csv.reader(f)
                for row in reader:
                    try:
                        InformationCart.objects.get_or_create(
                            name=row[0], type=row[1]
                        )
                    except Exception as e:
                        logger.error(
                            f"error in uploading: {file} - {row[0]}: {e}"
                        )
                logger.info(f"{file}upload ended")
