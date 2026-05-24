"""Точка входа в Telegram-бот по обучению созданию видео с помощью ИИ."""
from __future__ import annotations

import logging

from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    PollAnswerHandler,
)

from bot.config import load_settings, setup_logging
from bot.handlers import help as help_handler
from bot.handlers import lessons, quiz, start, tips, tools

logger = logging.getLogger(__name__)


def build_application(token: str):
    app = ApplicationBuilder().token(token).build()

    # Команды
    app.add_handler(CommandHandler("start", start.start))
    app.add_handler(CommandHandler("menu", start.start))
    app.add_handler(CommandHandler("lessons", lessons.show_lessons_menu))
    app.add_handler(CommandHandler("tools", tools.show_tools_menu))
    app.add_handler(CommandHandler("tips", tips.show_tips_menu))
    app.add_handler(CommandHandler("quiz", quiz.show_quiz_menu))
    app.add_handler(CommandHandler("help", help_handler.show_help))

    # Колбэки от inline-кнопок: маршрутизируем по префиксу
    app.add_handler(CallbackQueryHandler(start.on_main_menu, pattern=r"^menu:"))
    app.add_handler(CallbackQueryHandler(lessons.on_lesson_callback, pattern=r"^lesson:"))
    app.add_handler(CallbackQueryHandler(tools.on_tool_callback, pattern=r"^tool:"))
    app.add_handler(CallbackQueryHandler(tips.on_tip_callback, pattern=r"^tip:"))
    app.add_handler(CallbackQueryHandler(quiz.on_quiz_callback, pattern=r"^quiz:"))

    # Ответы на встроенные опросы Telegram (для квизов)
    app.add_handler(PollAnswerHandler(quiz.on_poll_answer))

    return app


def main() -> None:
    settings = load_settings()
    setup_logging(settings.log_level)
    logger.info("Запускаю AI Video School Bot...")

    app = build_application(settings.bot_token)
    app.run_polling(allowed_updates=None)


if __name__ == "__main__":
    main()
