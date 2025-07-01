# bot/management/commands/runbot.py

from django.core.management.base import BaseCommand
import os
import sys

class Command(BaseCommand):
    help = 'Запускает Telegram бота'

    def handle(self, *args, **options):
        # Чтобы не дублировать код, мы просто импортируем и запускаем функцию main() из bot/telegram_bot.py
        # Но нам нужно убедиться, что PYTHONPATH правильно настроен: добавляем корень проекта в sys.path
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
        if project_root not in sys.path:
            sys.path.insert(0, project_root)

        # Импортируем скрипт и запускаем main()
        from bot.telegram_bot import main
        main()
