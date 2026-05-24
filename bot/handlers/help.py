"""Команда /help и экран справки."""
from __future__ import annotations

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from bot import keyboards

HELP_TEXT = (
    "*ℹ️ Справка*\n\n"
    "Команды бота:\n"
    "• /start — главное меню\n"
    "• /lessons — модули курса\n"
    "• /tools — каталог ИИ-инструментов\n"
    "• /tips — советы и приёмы\n"
    "• /quiz — пройти квиз\n"
    "• /help — эта справка\n\n"
    "*Как учиться:*\n"
    "1. Пройди модули курса по порядку (📚 Курс).\n"
    "2. После каждого модуля закрепи знания квизом.\n"
    "3. Смотри каталог инструментов — там описание и ссылки.\n"
    "4. Применяй советы из раздела 💡 в реальных проектах.\n\n"
    "Удачных генераций! ✨"
)


async def show_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(
            text=HELP_TEXT,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=keyboards.back_to_main_kb(),
        )
    else:
        await update.message.reply_text(
            text=HELP_TEXT,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=keyboards.back_to_main_kb(),
        )
