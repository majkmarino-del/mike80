"""Middleware: обязательная подписка на канал.

Регистрируется как ``TypeHandler`` в группе ``-1`` — запускается перед всеми
прочими хендлерами. Если пользователь не подписан на ``settings.required_channel``,
показываем экран-«гейт» и прерываем дальнейшую обработку через
``ApplicationHandlerStop``.
"""
from __future__ import annotations

import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.error import TelegramError
from telegram.ext import ApplicationHandlerStop, ContextTypes

logger = logging.getLogger(__name__)

# Telegram считает подписчиками тех, у кого статус один из этих.
_SUBSCRIBED_STATUSES = {"creator", "administrator", "member"}

# Колбэки, которые должны проходить ДО проверки подписки
# (иначе пользователь не сможет нажать «я подписался — проверить»).
_WHITELISTED_CALLBACK_PREFIXES = ("sub:",)


def _channel_url(channel: str) -> str:
    """Возвращает HTTPS-ссылку на канал по его @username, ID или url."""
    channel = channel.strip()
    if channel.startswith("https://") or channel.startswith("http://"):
        return channel
    if channel.startswith("@"):
        return f"https://t.me/{channel[1:]}"
    if channel.lstrip("-").isdigit():
        # Числовой ID канала — публичной ссылки нет, ведём на t.me с поиском.
        # Для приватных каналов проще использовать invite-ссылку через REQUIRED_CHANNEL_URL.
        return "https://t.me/"
    return f"https://t.me/{channel}"


def gate_keyboard(channel: str, channel_url: str | None = None) -> InlineKeyboardMarkup:
    url = channel_url or _channel_url(channel)
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("📢 Перейти к каналу", url=url)],
            [InlineKeyboardButton("✅ Я подписался — проверить", callback_data="sub:check")],
        ]
    )


GATE_TEXT = (
    "🔒 *Доступ только для подписчиков*\n\n"
    "Этот бот — обучающий курс по созданию видео с помощью ИИ. "
    "Чтобы открыть уроки, каталог инструментов, советы и квизы, "
    "подпишись на наш канал.\n\n"
    "👉 Подпишись и нажми *«✅ Я подписался — проверить»*."
)


async def is_user_subscribed(bot, channel: str, user_id: int) -> bool:
    """Проверяет, состоит ли пользователь в указанном канале.

    Бот должен быть участником канала (обычно админом), иначе Telegram
    вернёт ошибку доступа — в этом случае считаем, что подписки нет.
    """
    try:
        member = await bot.get_chat_member(chat_id=channel, user_id=user_id)
    except TelegramError as exc:
        logger.warning(
            "Не удалось проверить подписку (channel=%s, user=%s): %s",
            channel,
            user_id,
            exc,
        )
        return False
    return member.status in _SUBSCRIBED_STATUSES


async def _send_gate(update: Update, channel: str, channel_url: str | None) -> None:
    keyboard = gate_keyboard(channel, channel_url)
    if update.callback_query is not None:
        try:
            await update.callback_query.edit_message_text(
                text=GATE_TEXT,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=keyboard,
            )
        except TelegramError:
            # Сообщение могло быть удалено или текст совпадает — присылаем новое.
            await update.callback_query.message.reply_text(
                text=GATE_TEXT,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=keyboard,
            )
        await update.callback_query.answer()
    elif update.message is not None:
        await update.message.reply_text(
            text=GATE_TEXT,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=keyboard,
        )


async def subscription_gate(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Pre-handler: пускает в бот только подписчиков канала."""
    settings = context.application.bot_data.get("settings")
    if settings is None or not settings.required_channel:
        return  # gating отключён (settings не пробросили или канал не задан)

    user = update.effective_user
    if user is None:
        # Например, обновления типа poll — пропускаем.
        return

    # Whitelisted callbacks (проверка подписки сама по себе).
    if update.callback_query is not None and update.callback_query.data:
        if any(
            update.callback_query.data.startswith(prefix)
            for prefix in _WHITELISTED_CALLBACK_PREFIXES
        ):
            return

    if await is_user_subscribed(context.bot, settings.required_channel, user.id):
        return

    await _send_gate(update, settings.required_channel, settings.required_channel_url)
    raise ApplicationHandlerStop


async def on_subscription_check(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Колбэк ``sub:check``: пользователь утверждает, что подписался."""
    query = update.callback_query
    if query is None:
        return

    settings = context.application.bot_data.get("settings")
    user = update.effective_user
    if settings is None or not settings.required_channel or user is None:
        await query.answer()
        return

    if await is_user_subscribed(context.bot, settings.required_channel, user.id):
        await query.answer("✅ Подписка подтверждена!", show_alert=False)
        # Импорт здесь, чтобы не ловить циклический импорт на старте модуля.
        from bot.handlers import start as start_handler

        await start_handler.start(update, context)
    else:
        await query.answer(
            "Подписка не найдена. Подпишись на канал и нажми ещё раз.",
            show_alert=True,
        )
