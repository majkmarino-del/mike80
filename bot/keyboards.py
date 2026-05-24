"""Inline-клавиатуры для всех экранов бота.

Соглашение по callback_data:
    menu:<screen>                       — главное меню
    lesson:list                         — список модулей
    lesson:m:<module_id>                — конкретный модуль (список уроков)
    lesson:l:<module_id>:<lesson_id>    — конкретный урок
    tool:list                           — список категорий
    tool:c:<category_id>                — список инструментов в категории
    tool:t:<category_id>:<tool_id>      — конкретный инструмент
    tip:list                            — список советов
    tip:t:<tip_id>                      — конкретный совет
    quiz:list                           — список квизов
    quiz:start:<quiz_id>                — запустить квиз
"""
from __future__ import annotations

from typing import List

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from bot.content.lessons import Lesson, Module, list_modules
from bot.content.quizzes import list_quizzes
from bot.content.tips import list_tips
from bot.content.tools import Tool, get_categories, get_tools_by_category


def main_menu_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("📚 Курс", callback_data="lesson:list")],
            [InlineKeyboardButton("🛠 ИИ-инструменты", callback_data="tool:list")],
            [InlineKeyboardButton("💡 Советы и приёмы", callback_data="tip:list")],
            [InlineKeyboardButton("❓ Квиз", callback_data="quiz:list")],
            [InlineKeyboardButton("ℹ️ Справка", callback_data="menu:help")],
        ]
    )


def back_to_main_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton("⬅️ В главное меню", callback_data="menu:main")]]
    )


# ---------- Уроки ----------

def modules_kb() -> InlineKeyboardMarkup:
    rows: List[List[InlineKeyboardButton]] = []
    for module in list_modules():
        rows.append(
            [InlineKeyboardButton(module.title, callback_data=f"lesson:m:{module.id}")]
        )
    rows.append([InlineKeyboardButton("⬅️ В главное меню", callback_data="menu:main")])
    return InlineKeyboardMarkup(rows)


def module_lessons_kb(module: Module) -> InlineKeyboardMarkup:
    rows: List[List[InlineKeyboardButton]] = []
    for lesson in module.lessons:
        rows.append(
            [
                InlineKeyboardButton(
                    f"📖 {lesson.title}",
                    callback_data=f"lesson:l:{module.id}:{lesson.id}",
                )
            ]
        )
    rows.append(
        [InlineKeyboardButton("⬅️ К модулям", callback_data="lesson:list")]
    )
    return InlineKeyboardMarkup(rows)


def lesson_nav_kb(
    module: Module, current: Lesson, prev_lesson: Lesson | None, next_lesson: Lesson | None
) -> InlineKeyboardMarkup:
    nav_row: List[InlineKeyboardButton] = []
    if prev_lesson is not None:
        nav_row.append(
            InlineKeyboardButton(
                "⬅️ Назад",
                callback_data=f"lesson:l:{module.id}:{prev_lesson.id}",
            )
        )
    if next_lesson is not None:
        nav_row.append(
            InlineKeyboardButton(
                "Вперёд ➡️",
                callback_data=f"lesson:l:{module.id}:{next_lesson.id}",
            )
        )

    rows: List[List[InlineKeyboardButton]] = []
    if nav_row:
        rows.append(nav_row)
    rows.append(
        [
            InlineKeyboardButton(
                "📚 К урокам модуля", callback_data=f"lesson:m:{module.id}"
            )
        ]
    )
    rows.append([InlineKeyboardButton("🏠 Главное меню", callback_data="menu:main")])
    return InlineKeyboardMarkup(rows)


# ---------- Инструменты ----------

def tool_categories_kb() -> InlineKeyboardMarkup:
    rows: List[List[InlineKeyboardButton]] = []
    for cat in get_categories():
        rows.append(
            [
                InlineKeyboardButton(
                    f"{cat.emoji} {cat.title}",
                    callback_data=f"tool:c:{cat.id}",
                )
            ]
        )
    rows.append([InlineKeyboardButton("⬅️ В главное меню", callback_data="menu:main")])
    return InlineKeyboardMarkup(rows)


def tools_in_category_kb(category_id: str) -> InlineKeyboardMarkup:
    rows: List[List[InlineKeyboardButton]] = []
    for tool in get_tools_by_category(category_id):
        rows.append(
            [
                InlineKeyboardButton(
                    tool.name,
                    callback_data=f"tool:t:{category_id}:{tool.id}",
                )
            ]
        )
    rows.append(
        [InlineKeyboardButton("⬅️ К категориям", callback_data="tool:list")]
    )
    return InlineKeyboardMarkup(rows)


def tool_detail_kb(tool: Tool) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("🔗 Открыть сайт", url=tool.url)],
            [
                InlineKeyboardButton(
                    "⬅️ К инструментам",
                    callback_data=f"tool:c:{tool.category}",
                )
            ],
            [InlineKeyboardButton("🏠 Главное меню", callback_data="menu:main")],
        ]
    )


# ---------- Советы ----------

def tips_kb() -> InlineKeyboardMarkup:
    rows: List[List[InlineKeyboardButton]] = []
    for tip in list_tips():
        rows.append(
            [InlineKeyboardButton(tip.title, callback_data=f"tip:t:{tip.id}")]
        )
    rows.append([InlineKeyboardButton("⬅️ В главное меню", callback_data="menu:main")])
    return InlineKeyboardMarkup(rows)


def tip_detail_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("⬅️ К советам", callback_data="tip:list")],
            [InlineKeyboardButton("🏠 Главное меню", callback_data="menu:main")],
        ]
    )


# ---------- Квизы ----------

def quizzes_kb() -> InlineKeyboardMarkup:
    rows: List[List[InlineKeyboardButton]] = []
    for quiz in list_quizzes():
        rows.append(
            [
                InlineKeyboardButton(
                    f"❓ {quiz.title}",
                    callback_data=f"quiz:start:{quiz.id}",
                )
            ]
        )
    rows.append([InlineKeyboardButton("⬅️ В главное меню", callback_data="menu:main")])
    return InlineKeyboardMarkup(rows)
