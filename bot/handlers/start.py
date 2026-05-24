"""Команда /start и главное меню."""
from __future__ import annotations

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from bot import keyboards
from bot.handlers import help as help_handler

WELCOME_TEXT = (
    "🎬 *AI Video School*\n"
    "Привет, {name}! Я помогу тебе освоить создание видео с помощью ИИ.\n\n"
    "Что внутри:\n"
    "📚 *Курс* — 5 модулей: основы, инструменты, промпты, звук, рецепты\n"
    "🛠 *ИИ-инструменты* — каталог сервисов с описанием и ценами\n"
    "💡 *Советы* — практические приёмы для лучшего результата\n"
    "❓ *Квиз* — проверь свои знания\n\n"
    "Выбирай раздел в меню ниже 👇"
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    name = user.first_name if user else "друг"
    text = WELCOME_TEXT.format(name=name)

    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(
            text=text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=keyboards.main_menu_kb(),
        )
    else:
        await update.message.reply_text(
            text=text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=keyboards.main_menu_kb(),
        )


async def on_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик callback_data вида menu:<screen>."""
    query = update.callback_query
    if not query or not query.data:
        return

    _, screen = query.data.split(":", 1)

    if screen == "main":
        await start(update, context)
        return
    if screen == "help":
        await help_handler.show_help(update, context)
        return

    await query.answer("Неизвестный пункт меню.")
