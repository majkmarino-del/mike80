"""Хендлеры для каталога ИИ-инструментов."""
from __future__ import annotations

import logging

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from bot import keyboards
from bot.content.tools import (
    get_categories,
    get_tool,
    get_tools_by_category,
)

logger = logging.getLogger(__name__)


async def show_tools_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    cats = get_categories()
    text = (
        "*🛠 ИИ-инструменты для видео*\n\n"
        "Каталог разделён на категории. Выбирай нужное направление:\n\n"
        + "\n".join(f"{c.emoji} *{c.title}*" for c in cats)
    )
    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(
            text=text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=keyboards.tool_categories_kb(),
        )
    else:
        await update.message.reply_text(
            text=text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=keyboards.tool_categories_kb(),
        )


async def _show_category(update: Update, category_id: str) -> None:
    tools = get_tools_by_category(category_id)
    if not tools:
        await update.callback_query.answer("Категория пуста.")
        return

    cat = next((c for c in get_categories() if c.id == category_id), None)
    title = f"{cat.emoji} {cat.title}" if cat else "Категория"
    text = (
        f"*{title}*\n\n"
        + "\n\n".join(
            f"• *{t.name}*\n  _{t.pricing}_" for t in tools
        )
        + "\n\nВыбери сервис, чтобы увидеть подробности:"
    )
    await update.callback_query.edit_message_text(
        text=text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=keyboards.tools_in_category_kb(category_id),
    )


async def _show_tool(update: Update, category_id: str, tool_id: str) -> None:
    tool = get_tool(category_id, tool_id)
    if not tool:
        await update.callback_query.answer("Инструмент не найден.")
        return

    text = (
        f"*{tool.name}*\n\n"
        f"{tool.description}\n\n"
        f"💵 *Цена:* {tool.pricing}\n"
        f"🔗 [Открыть сайт]({tool.url})"
    )
    await update.callback_query.edit_message_text(
        text=text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=keyboards.tool_detail_kb(tool),
        disable_web_page_preview=True,
    )


async def on_tool_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обрабатывает: tool:list | tool:c:<cat> | tool:t:<cat>:<tool>."""
    query = update.callback_query
    if not query or not query.data:
        return
    await query.answer()

    parts = query.data.split(":")
    action = parts[1] if len(parts) > 1 else ""

    try:
        if action == "list":
            await show_tools_menu(update, context)
        elif action == "c" and len(parts) >= 3:
            await _show_category(update, parts[2])
        elif action == "t" and len(parts) >= 4:
            await _show_tool(update, parts[2], parts[3])
        else:
            await query.answer("Неизвестная команда.")
    except Exception:  # noqa: BLE001
        logger.exception("Ошибка в on_tool_callback (data=%s)", query.data)
        await query.answer("Что-то пошло не так. Попробуйте ещё раз.")
