"""Квизы для проверки знаний."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass(frozen=True)
class Question:
    text: str
    options: List[str]
    correct_index: int
    explanation: str


@dataclass(frozen=True)
class Quiz:
    id: str
    title: str
    description: str
    questions: List[Question]


QUIZZES: Dict[str, Quiz] = {
    "basics": Quiz(
        id="basics",
        title="Основы AI-видео",
        description="5 вопросов на базовые термины и пайплайн.",
        questions=[
            Question(
                text="Что такое seed в генерации видео?",
                options=[
                    "Скорость рендеринга",
                    "Число, фиксирующее случайность генерации",
                    "Длина видео в секундах",
                    "Соотношение сторон кадра",
                ],
                correct_index=1,
                explanation=(
                    "Seed — это число, инициализирующее генератор случайных чисел. "
                    "Один и тот же seed + промпт = очень похожий результат."
                ),
            ),
            Question(
                text="Какое соотношение сторон у Reels и Shorts?",
                options=["16:9", "1:1", "9:16", "4:3"],
                correct_index=2,
                explanation="Вертикальное 9:16 — стандарт для Reels, Shorts и TikTok.",
            ),
            Question(
                text="Что такое image-to-video?",
                options=[
                    "Конвертация видео в набор картинок",
                    "Оживление статичной картинки в видеоклип",
                    "Сжатие видео для соцсетей",
                    "Перевод субтитров",
                ],
                correct_index=1,
                explanation=(
                    "Image-to-video — это превращение одного или нескольких кадров "
                    "в видеоклип с заданным движением."
                ),
            ),
            Question(
                text="Сколько секунд оптимально для одного клипа в современных моделях?",
                options=["1–2 секунды", "4–8 секунд", "30–60 секунд", "Несколько минут"],
                correct_index=1,
                explanation=(
                    "Большинство моделей выдают качественный результат на 4–8 сек. "
                    "Длинные ролики собираются из последовательности коротких сцен."
                ),
            ),
            Question(
                text="Что такое lip-sync?",
                options=[
                    "Синхронизация музыки с видео",
                    "Синхронизация губ персонажа с озвучкой",
                    "Цветокоррекция кожи",
                    "Замедление кадров",
                ],
                correct_index=1,
                explanation=(
                    "Lip-sync — это синхронизация артикуляции (движения губ) "
                    "персонажа с аудиодорожкой. Используется в HeyGen, D-ID, Hedra."
                ),
            ),
        ],
    ),
    "tools": Quiz(
        id="tools",
        title="Инструменты",
        description="5 вопросов про сервисы и их особенности.",
        questions=[
            Question(
                text="Какой инструмент лучше всего подходит для контроля движения камеры?",
                options=["Pika", "Runway Gen-3", "Suno", "ElevenLabs"],
                correct_index=1,
                explanation=(
                    "Runway Gen-3 имеет Director Mode и Motion Brush — "
                    "продвинутый контроль направления и скорости камеры."
                ),
            ),
            Question(
                text="Чем известен ElevenLabs?",
                options=[
                    "Генерацией видео",
                    "Синтезом и клонированием голоса",
                    "Цветокоррекцией",
                    "Создание 3D-моделей",
                ],
                correct_index=1,
                explanation=(
                    "ElevenLabs — лидер в TTS (text-to-speech) и клонировании "
                    "голоса с поддержкой 30+ языков."
                ),
            ),
            Question(
                text="Что генерирует Suno?",
                options=[
                    "Видеоклипы",
                    "Целые песни с вокалом",
                    "3D-сцены",
                    "Логотипы",
                ],
                correct_index=1,
                explanation=(
                    "Suno создаёт песни с вокалом и инструменталом по текстовому "
                    "описанию или своим стихам."
                ),
            ),
            Question(
                text="Для каких задач лучше всего HeyGen?",
                options=[
                    "Анимация пейзажей",
                    "Говорящие аватары и дубляж на разных языках",
                    "Музыкальные клипы",
                    "Спецэффекты взрывов",
                ],
                correct_index=1,
                explanation=(
                    "HeyGen — это фотореалистичные аватары-ведущие и автоматический "
                    "дубляж видео на 40+ языков с сохранением голоса."
                ),
            ),
            Question(
                text="Какой бесплатный редактор удобнее всего для Reels?",
                options=["DaVinci Resolve", "Premiere Pro", "CapCut", "After Effects"],
                correct_index=2,
                explanation=(
                    "CapCut бесплатный, имеет AI-субтитры, удаление фона и шаблоны "
                    "под вертикальные форматы."
                ),
            ),
        ],
    ),
    "prompting": Quiz(
        id="prompting",
        title="Промпт-инжиниринг",
        description="5 вопросов про промпты для видео.",
        questions=[
            Question(
                text="Какая длина промпта обычно даёт лучший результат?",
                options=[
                    "5–10 слов",
                    "30–60 слов",
                    "200+ слов",
                    "Длина не имеет значения",
                ],
                correct_index=1,
                explanation=(
                    "30–60 слов — золотая середина: достаточно деталей, но модель "
                    "не «забывает» начало."
                ),
            ),
            Question(
                text="Что означает команда `dolly-in`?",
                options=[
                    "Камера вращается вокруг оси",
                    "Камера наезжает на объект по оси",
                    "Камера наклоняется вверх",
                    "Резкий разворот камеры",
                ],
                correct_index=1,
                explanation=(
                    "Dolly-in — наезд камеры по оси к объекту, противоположность "
                    "dolly-out (отъезд)."
                ),
            ),
            Question(
                text="Что лучше НЕ помещать в один промпт?",
                options=[
                    "Описание света",
                    "Несколько разных субъектов с разными действиями",
                    "Стиль и атмосферу",
                    "Тип камеры",
                ],
                correct_index=1,
                explanation=(
                    "Несколько субъектов с разными действиями путают модель. "
                    "Разбивайте такие сцены на отдельные клипы."
                ),
            ),
            Question(
                text="Зачем нужен negative prompt?",
                options=[
                    "Чтобы ускорить генерацию",
                    "Чтобы указать, чего НЕ должно быть в кадре",
                    "Чтобы сэкономить токены",
                    "Для перевода на другой язык",
                ],
                correct_index=1,
                explanation=(
                    "Negative prompt помогает убрать нежелательные элементы: "
                    "водяные знаки, лишние конечности, текст, артефакты."
                ),
            ),
            Question(
                text="Какой свет даёт «киношную» картинку?",
                options=[
                    "Прямой полуденный свет",
                    "Golden hour (час до заката)",
                    "Свет от лампы накаливания сверху",
                    "Свет вспышки в лоб",
                ],
                correct_index=1,
                explanation=(
                    "Golden hour даёт тёплый направленный свет с длинными тенями — "
                    "именно за это его любят кинооператоры."
                ),
            ),
        ],
    ),
}


def list_quizzes() -> List[Quiz]:
    return list(QUIZZES.values())


def get_quiz(quiz_id: str) -> Quiz | None:
    return QUIZZES.get(quiz_id)
