"""Хендлеры для раздела «Квиз».

Используем нативные Telegram-poll'ы типа `quiz`: Telegram сам подсвечивает
правильный ответ и показывает объяснение.
"""
from __future__ import annotations

import logging

from telegram import Update
from telegram.constants import ParseMode, PollType
from telegram.ext import ContextTypes

from bot import keyboards
from bot.content.quizzes import Quiz, get_quiz, list_quizzes

logger = logging.getLogger(__name__)

# Лимит Telegram на explanation в poll — 200 символов.
_EXPLANATION_LIMIT = 200


def _trim_explanation(text: str) -> str:
    if len(text) <= _EXPLANATION_LIMIT:
        return text
    return text[: _EXPLANATION_LIMIT - 1] + "…"


async def show_quiz_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = (
        "*❓ Квизы*\n\n"
        "Проверь свои знания. После каждого вопроса бот покажет правильный "
        "ответ и пояснение.\n\n"
        + "\n".join(f"• *{q.title}* — {q.description}" for q in list_quizzes())
        + "\n\nВыбери квиз:"
    )
    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(
            text=text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=keyboards.quizzes_kb(),
        )
    else:
        await update.message.reply_text(
            text=text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=keyboards.quizzes_kb(),
        )


async def _start_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE, quiz_id: str) -> None:
    quiz = get_quiz(quiz_id)
    if not quiz:
        await update.callback_query.answer("Квиз не найден.")
        return

    chat_id = update.effective_chat.id
    await update.callback_query.answer()

    # Заменяем текст исходного сообщения на «обложку» квиза.
    await update.callback_query.edit_message_text(
        text=(
            f"*🚀 Квиз: {quiz.title}*\n\n"
            f"Вопросов: {len(quiz.questions)}\n\n"
            f"Сейчас пришлю их по одному 👇"
        ),
        parse_mode=ParseMode.MARKDOWN,
    )

    await _send_quiz_polls(context, chat_id, quiz)

    # Финальное сообщение с навигацией обратно.
    await context.bot.send_message(
        chat_id=chat_id,
        text="✅ Квиз завершён! Молодец, что прошёл до конца.",
        reply_markup=keyboards.main_menu_kb(),
    )


async def _send_quiz_polls(
    context: ContextTypes.DEFAULT_TYPE, chat_id: int, quiz: Quiz
) -> None:
    for idx, question in enumerate(quiz.questions, start=1):
        await context.bot.send_poll(
            chat_id=chat_id,
            question=f"{idx}/{len(quiz.questions)}. {question.text}",
            options=question.options,
            type=PollType.QUIZ,
            correct_option_id=question.correct_index,
            explanation=_trim_explanation(question.explanation),
            is_anonymous=False,
        )


async def on_quiz_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обрабатывает: quiz:list | quiz:start:<id>."""
    query = update.callback_query
    if not query or not query.data:
        return

    parts = query.data.split(":")
    action = parts[1] if len(parts) > 1 else ""

    try:
        if action == "list":
            await show_quiz_menu(update, context)
        elif action == "start" and len(parts) >= 3:
            await _start_quiz(update, context, parts[2])
        else:
            await query.answer("Неизвестная команда.")
    except Exception:  # noqa: BLE001
        logger.exception("Ошибка в on_quiz_callback (data=%s)", query.data)
        await query.answer("Что-то пошло не так. Попробуйте ещё раз.")


async def on_poll_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Логируем ответы пользователей на poll'ы. Telegram сам показывает результат."""
    answer = update.poll_answer
    if answer is None:
        return
    logger.info(
        "PollAnswer: user_id=%s, poll_id=%s, option_ids=%s",
        answer.user.id if answer.user else None,
        answer.poll_id,
        answer.option_ids,
    )
