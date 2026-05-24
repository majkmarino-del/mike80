"""Хендлеры для раздела «Курс» (модули и уроки)."""
from __future__ import annotations

import logging

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from bot import keyboards
from bot.content.lessons import get_lesson, get_module, list_modules

logger = logging.getLogger(__name__)


async def show_lessons_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = "*📚 Курс по AI-видео*\n\nВыбери модуль:\n\n" + "\n".join(
        f"• *{m.title}* — {m.description}" for m in list_modules()
    )
    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(
            text=text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=keyboards.modules_kb(),
        )
    else:
        await update.message.reply_text(
            text=text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=keyboards.modules_kb(),
        )


async def _show_module(update: Update, module_id: str) -> None:
    module = get_module(module_id)
    if not module:
        await update.callback_query.answer("Модуль не найден.")
        return

    text = (
        f"*{module.title}*\n"
        f"_{module.description}_\n\n"
        f"Уроки модуля:\n"
        + "\n".join(f"• {l.title}" for l in module.lessons)
        + "\n\nВыбери урок:"
    )
    await update.callback_query.edit_message_text(
        text=text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=keyboards.module_lessons_kb(module),
    )


async def _show_lesson(update: Update, module_id: str, lesson_id: str) -> None:
    module = get_module(module_id)
    lesson = get_lesson(module_id, lesson_id)
    if not module or not lesson:
        await update.callback_query.answer("Урок не найден.")
        return

    # prev/next для навигации по урокам внутри модуля
    lessons = module.lessons
    idx = next((i for i, l in enumerate(lessons) if l.id == lesson.id), 0)
    prev_lesson = lessons[idx - 1] if idx > 0 else None
    next_lesson = lessons[idx + 1] if idx + 1 < len(lessons) else None

    text = (
        f"*{module.title}* · урок {idx + 1}/{len(lessons)}\n\n"
        f"{lesson.body}"
    )
    await update.callback_query.edit_message_text(
        text=text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=keyboards.lesson_nav_kb(module, lesson, prev_lesson, next_lesson),
        disable_web_page_preview=True,
    )


async def on_lesson_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обрабатывает callback_data: lesson:list | lesson:m:<id> | lesson:l:<m>:<l>."""
    query = update.callback_query
    if not query or not query.data:
        return
    await query.answer()

    parts = query.data.split(":")
    # parts[0] == 'lesson'
    action = parts[1] if len(parts) > 1 else ""

    try:
        if action == "list":
            await show_lessons_menu(update, context)
        elif action == "m" and len(parts) >= 3:
            await _show_module(update, parts[2])
        elif action == "l" and len(parts) >= 4:
            await _show_lesson(update, parts[2], parts[3])
        else:
            await query.answer("Неизвестная команда.")
    except Exception:  # noqa: BLE001
        logger.exception("Ошибка в on_lesson_callback (data=%s)", query.data)
        await query.answer("Что-то пошло не так. Попробуйте ещё раз.")
