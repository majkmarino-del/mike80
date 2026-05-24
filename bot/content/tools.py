"""Каталог ИИ-инструментов для создания видео."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass(frozen=True)
class Tool:
    id: str
    name: str
    category: str
    description: str
    pricing: str
    url: str


@dataclass(frozen=True)
class Category:
    id: str
    title: str
    emoji: str


CATEGORIES: List[Category] = [
    Category("t2v", "Text-to-Video", "🎬"),
    Category("i2v", "Image-to-Video", "🖼"),
    Category("avatar", "Аватары и липсинк", "🗣"),
    Category("voice", "Голос и звук", "🎙"),
    Category("music", "Музыка", "🎵"),
    Category("edit", "Монтаж и пост", "✂️"),
]


TOOLS: Dict[str, List[Tool]] = {
    "t2v": [
        Tool(
            id="sora",
            name="Sora (OpenAI)",
            category="t2v",
            description=(
                "Флагманская text-to-video модель. До 60 сек, отличная "
                "физика, удержание персонажа. Доступна в ChatGPT Plus/Pro."
            ),
            pricing="От $20/мес (ChatGPT Plus)",
            url="https://openai.com/sora",
        ),
        Tool(
            id="veo",
            name="Google Veo",
            category="t2v",
            description=(
                "Кинематографичные пейзажи и свет, сильное понимание "
                "промптов на русском. Доступ через Google AI / Vertex AI."
            ),
            pricing="Бесплатно на Gemini Advanced (триал)",
            url="https://deepmind.google/technologies/veo/",
        ),
        Tool(
            id="kling",
            name="Kling AI",
            category="t2v",
            description=(
                "Лучшее движение людей и животных, удачный баланс "
                "цена/качество. Поддержка text-to-video и image-to-video."
            ),
            pricing="Бесплатный тир + от $10/мес",
            url="https://klingai.com/",
        ),
        Tool(
            id="hailuo",
            name="Hailuo (MiniMax)",
            category="t2v",
            description=(
                "Быстрая генерация 6 сек, понимает русские промпты, "
                "щедрый бесплатный тир."
            ),
            pricing="Бесплатно с лимитами",
            url="https://hailuoai.video/",
        ),
    ],
    "i2v": [
        Tool(
            id="runway",
            name="Runway Gen-3",
            category="i2v",
            description=(
                "Лучший контроль камеры (Director Mode, Motion Brush). "
                "Image-to-video и video-to-video, 10 сек на клип."
            ),
            pricing="От $15/мес",
            url="https://runwayml.com/",
        ),
        Tool(
            id="pika",
            name="Pika 2.0",
            category="i2v",
            description=(
                "Простой UI, фирменные эффекты Pikaffects (взрыв, "
                "превращение, плавление). Хорош для соцсетей."
            ),
            pricing="Бесплатный тир + от $10/мес",
            url="https://pika.art/",
        ),
        Tool(
            id="luma",
            name="Luma Dream Machine",
            category="i2v",
            description=(
                "Плавное движение, поддержка keyframes (старт + финиш). "
                "Умеет генерировать петли (loop)."
            ),
            pricing="Бесплатный тир + от $10/мес",
            url="https://lumalabs.ai/dream-machine",
        ),
    ],
    "avatar": [
        Tool(
            id="heygen",
            name="HeyGen",
            category="avatar",
            description=(
                "Фотореалистичные аватары, клонирование за 2 минуты, "
                "перевод и дубляж на 40+ языков с сохранением голоса."
            ),
            pricing="Бесплатно 1 мин/мес + от $24/мес",
            url="https://www.heygen.com/",
        ),
        Tool(
            id="did",
            name="D-ID",
            category="avatar",
            description=(
                "Оживление портретов и фото. Хорошо для исторических "
                "кадров, мемов и презентаций."
            ),
            pricing="От $5.9/мес",
            url="https://www.d-id.com/",
        ),
        Tool(
            id="hedra",
            name="Hedra",
            category="avatar",
            description=(
                "Выразительная мимика по аудио. Загружаете фото и "
                "дорожку голоса — получаете говорящий портрет."
            ),
            pricing="Бесплатный тир",
            url="https://www.hedra.com/",
        ),
    ],
    "voice": [
        Tool(
            id="elevenlabs",
            name="ElevenLabs",
            category="voice",
            description=(
                "Эталон синтеза речи. Клонирование голоса, 30+ языков, "
                "управление эмоциями и стабильностью."
            ),
            pricing="Бесплатно 10к симв./мес + от $5/мес",
            url="https://elevenlabs.io/",
        ),
        Tool(
            id="playht",
            name="PlayHT",
            category="voice",
            description=(
                "Сотни голосов, дешевле ElevenLabs. Подойдёт для "
                "длинных аудиокниг и подкастов."
            ),
            pricing="От $19/мес",
            url="https://play.ht/",
        ),
    ],
    "music": [
        Tool(
            id="suno",
            name="Suno",
            category="music",
            description=(
                "Генерирует целые песни с вокалом по текстовому описанию "
                "и/или своим стихам. До 4 минут."
            ),
            pricing="Бесплатно 10 песен/день + от $10/мес",
            url="https://suno.com/",
        ),
        Tool(
            id="udio",
            name="Udio",
            category="music",
            description=(
                "Конкурент Suno, ставит акцент на чистоту звука и "
                "разнообразие жанров."
            ),
            pricing="Бесплатный тир + платные планы",
            url="https://www.udio.com/",
        ),
        Tool(
            id="mubert",
            name="Mubert",
            category="music",
            description=(
                "Генеративная фоновая музыка без копирайта, удобно "
                "для YouTube и подкастов."
            ),
            pricing="Бесплатный тир + от $14/мес",
            url="https://mubert.com/",
        ),
    ],
    "edit": [
        Tool(
            id="capcut",
            name="CapCut",
            category="edit",
            description=(
                "Бесплатный редактор от ByteDance. AI-субтитры, удаление "
                "фона, готовые шаблоны для Reels/TikTok."
            ),
            pricing="Бесплатно (Pro от $7.99/мес)",
            url="https://www.capcut.com/",
        ),
        Tool(
            id="davinci",
            name="DaVinci Resolve",
            category="edit",
            description=(
                "Профессиональный монтаж и цветокоррекция. Бесплатная "
                "версия покрывает 90% задач."
            ),
            pricing="Бесплатно (Studio $295 единоразово)",
            url="https://www.blackmagicdesign.com/products/davinciresolve",
        ),
        Tool(
            id="descript",
            name="Descript",
            category="edit",
            description=(
                "Монтаж видео через редактирование текстовой "
                "транскрипции. Удобно для подкастов и интервью."
            ),
            pricing="Бесплатный тир + от $12/мес",
            url="https://www.descript.com/",
        ),
        Tool(
            id="topaz",
            name="Topaz Video AI",
            category="edit",
            description=(
                "Апскейл видео до 4K/8K, увеличение FPS, удаление шума. "
                "Спасает низкокачественные исходники."
            ),
            pricing="$299 единоразово",
            url="https://www.topazlabs.com/topaz-video-ai",
        ),
    ],
}


def get_categories() -> List[Category]:
    return CATEGORIES


def get_tools_by_category(category_id: str) -> List[Tool]:
    return TOOLS.get(category_id, [])


def get_tool(category_id: str, tool_id: str) -> Tool | None:
    for tool in TOOLS.get(category_id, []):
        if tool.id == tool_id:
            return tool
    return None
