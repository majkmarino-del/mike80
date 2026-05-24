"""Точка входа в Telegram-бот по обучению созданию видео с помощью ИИ."""
from __future__ import annotations

import logging

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    PollAnswerHandler,
    TypeHandler,
)

from bot import middleware
from bot.config import Settings, load_settings, setup_logging
from bot.handlers import help as help_handler
from bot.handlers import lessons, quiz, start, tips, tools

logger = logging.getLogger(__name__)


def build_application(settings: Settings):
    app = ApplicationBuilder().token(settings.bot_token).build()

    # Делаем настройки доступными во всех хендлерах через context.application.bot_data
    app.bot_data["settings"] = settings

    # ----- Pre-handler: проверка подписки на канал -----
    # Группа -1 запускается раньше всех остальных хендлеров.
    # Если пользователь не подписан — middleware остановит дальнейшую обработку.
    app.add_handler(TypeHandler(Update, middleware.subscription_gate), group=-1)

    # Колбэк проверки подписки (должен идти ДО общего menu/lesson и т.д.,
    # но т.к. паттерны не пересекаются — порядок не критичен).
    app.add_handler(
        CallbackQueryHandler(middleware.on_subscription_check, pattern=r"^sub:check$")
    )

    # ----- Команды -----
    app.add_handler(CommandHandler("start", start.start))
    app.add_handler(CommandHandler("menu", start.start))
    app.add_handler(CommandHandler("lessons", lessons.show_lessons_menu))
    app.add_handler(CommandHandler("tools", tools.show_tools_menu))
    app.add_handler(CommandHandler("tips", tips.show_tips_menu))
    app.add_handler(CommandHandler("quiz", quiz.show_quiz_menu))
    app.add_handler(CommandHandler("help", help_handler.show_help))

    # ----- Колбэки от inline-кнопок: маршрутизация по префиксу -----
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
    logger.info(
        "Запускаю AI Video School Bot... required_channel=%s",
        settings.required_channel,
    )

    app = build_application(settings)
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
