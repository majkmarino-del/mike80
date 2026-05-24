"""Конфигурация бота: загрузка переменных окружения."""
from __future__ import annotations

import logging
import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    bot_token: str
    required_channel: str  # @username или числовой ID канала
    required_channel_url: str | None = None  # явный URL (нужен для приватных каналов)
    log_level: str = "INFO"


def load_settings() -> Settings:
    token = os.getenv("BOT_TOKEN", "").strip()
    if not token:
        raise RuntimeError(
            "BOT_TOKEN не задан. Скопируйте .env.example в .env и укажите токен бота."
        )

    channel = os.getenv("REQUIRED_CHANNEL", "").strip()
    if not channel:
        raise RuntimeError(
            "REQUIRED_CHANNEL не задан. Подписка на канал — обязательное условие "
            "работы бота. Укажите @username канала (или его числовой ID, "
            "начинающийся с -100) в .env."
        )

    channel_url = os.getenv("REQUIRED_CHANNEL_URL", "").strip() or None

    return Settings(
        bot_token=token,
        required_channel=channel,
        required_channel_url=channel_url,
        log_level=os.getenv("LOG_LEVEL", "INFO").upper(),
    )


def setup_logging(level: str) -> None:
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=getattr(logging, level, logging.INFO),
    )
    # Снижаем шум от httpx (используется внутри telegram-bot)
    logging.getLogger("httpx").setLevel(logging.WARNING)
