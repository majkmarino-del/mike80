"""Хендлеры для раздела «Советы»."""
from __future__ import annotations

import logging

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from bot import keyboards
from bot.content.tips import get_tip, list_tips

logger = logging.getLogger(__name__)


async def show_tips_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = (
        "*💡 Советы и приёмы*\n\n"
        "Подборка коротких практических заметок. Выбирай интересующую тему:\n\n"
        + "\n".join(f"• {t.title}" for t in list_tips())
    )
    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(
            text=text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=keyboards.tips_kb(),
        )
    else:
        await update.message.reply_text(
            text=text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=keyboards.tips_kb(),
        )


async def _show_tip(update: Update, tip_id: str) -> None:
    tip = get_tip(tip_id)
    if not tip:
        await update.callback_query.answer("Совет не найден.")
        return

    await update.callback_query.edit_message_text(
        text=tip.body,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=keyboards.tip_detail_kb(),
        disable_web_page_preview=True,
    )


async def on_tip_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обрабатывает: tip:list | tip:t:<id>."""
    query = update.callback_query
    if not query or not query.data:
        return
    await query.answer()

    parts = query.data.split(":")
    action = parts[1] if len(parts) > 1 else ""

    try:
        if action == "list":
            await show_tips_menu(update, context)
        elif action == "t" and len(parts) >= 3:
            await _show_tip(update, parts[2])
        else:
            await query.answer("Неизвестная команда.")
    except Exception:  # noqa: BLE001
        logger.exception("Ошибка в on_tip_callback (data=%s)", query.data)
        await query.answer("Что-то пошло не так. Попробуйте ещё раз.")
