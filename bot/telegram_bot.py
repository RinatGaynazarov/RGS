import os
import django
import sys
import logging
import asyncio
import pytz
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from asgiref.sync import sync_to_async

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RGS.settings')
django.setup()

from main.models import Product
from django.contrib.auth.models import User


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def sync_create_product(name, quantity, user):
    return Product.objects.create(name=name, quantity=quantity, user=user)


def sync_get_products():
    return list(Product.objects.order_by('created_at')[:10])


def sync_get_default_user():
    return User.objects.get_or_create(username='bot_user')


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я бот для создания и просмотра заявок.\n\n"
        "Доступные команды:\n"
        "/new <название> | <количество> — создать новую заявку\n"
        "/list — посмотреть список последних заявок\n"
        "/help — показать эту подсказку"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Список доступных команд:\n"
        "/new <название> | <количество> — создать новую заявку\n"
        "/list — показать последние 10 заявок\n"
        "/help — подсказка по командам"
    )


async def new_zayavka(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        _, args = update.message.text.split(' ', 1)
        name, quantity_str = [part.strip() for part in args.split('|')]

        if not name or not quantity_str.isdigit():
            raise ValueError()

        quantity = int(quantity_str)
        user, created = await sync_to_async(sync_get_default_user)()

        z = await sync_to_async(sync_create_product)(name=name, quantity=quantity, user=user)

        await update.message.reply_text(
            f"✔ Заявка создана:\nID: {z.id}\n"
            f"Название: {z.name}\nКоличество: {z.quantity}"
        )
    except (ValueError, IndexError):
        await update.message.reply_text(
            "Неверный формат команды. Используйте:\n"
            "/new <название> | <количество>\n"
            "Пример: /new Яблоки | 5"
        )


async def list_zayavki(update: Update, context: ContextTypes.DEFAULT_TYPE):
    products = await sync_to_async(sync_get_products)()
    if not products:
        await update.message.reply_text("Пока нет ни одной заявки.")
        return

    response = ["Последние 10 заявок:"]
    for p in products:
        dt = p.created_at.astimezone(pytz.timezone('Europe/Moscow'))
        response.append(f"#{p.id}: {p.name} ({p.quantity}) — {dt.strftime('%Y-%m-%d %H:%M')}")

    await update.message.reply_text("\n".join(response))


async def unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Извините, я не понимаю эту команду.\n"
        "Напишите /help для списка доступных команд."
    )


async def run_bot():
    handlers = [
        CommandHandler("start", start),
        CommandHandler("help", help_command),
        CommandHandler("new", new_zayavka),
        CommandHandler("list", list_zayavki),
        MessageHandler(filters.COMMAND, unknown_command)
    ]

    application = ApplicationBuilder() \
        .token("7737370813:AAGIFaMkxFVY9JolNZrjGEOikrXH4ZwL-DM") \
        .build()

    for handler in handlers:
        application.add_handler(handler)

    await application.initialize()
    await application.start()
    await application.updater.start_polling()
    logger.info("Бот запущен и работает...")

    while True:
        await asyncio.sleep(3600)


if __name__ == "__main__":
    try:

        asyncio.run(run_bot())
    except KeyboardInterrupt:
        logger.info("Бот остановлен по запросу пользователя")
    except Exception as e:
        logger.error(f"Ошибка: {str(e)}", exc_info=True)
    finally:
        logger.info("Работа бота завершена")