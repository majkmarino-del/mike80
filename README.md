# 🎬 AI Video School Bot

Telegram-бот для обучения созданию видео с помощью искусственного интеллекта.

## Что внутри

- 📚 **5 модулей обучения** — от основ до продвинутых техник
- 🛠 **Каталог ИИ-инструментов** — Sora, Runway, Pika, Kling, HeyGen, ElevenLabs и др.
- ❓ **Квизы** для проверки знаний после каждого модуля
- 💡 **Советы по промптингу** для генерации видео
- 🚀 **Готовые рецепты** под разные задачи (Reels, YouTube Shorts, рекламные ролики)

## Структура проекта

```
mike80/
├── main.py                    # Точка входа
├── requirements.txt
├── .env.example
└── bot/
    ├── config.py              # Загрузка переменных окружения
    ├── keyboards.py           # Inline-клавиатуры
    ├── handlers/              # Обработчики команд и колбэков
    │   ├── start.py
    │   ├── lessons.py
    │   ├── quiz.py
    │   ├── tools.py
    │   └── tips.py
    └── content/               # Учебный контент
        ├── lessons.py
        ├── quizzes.py
        ├── tools.py
        └── tips.py
```

## Запуск

1. Создайте бота через [@BotFather](https://t.me/BotFather) и получите токен.
2. Скопируйте файл с переменными окружения:
   ```bash
   cp .env.example .env
   ```
3. Вставьте токен в `.env`:
   ```
   BOT_TOKEN=123456:ABC-DEF...
   ```
4. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```
5. Запустите:
   ```bash
   python main.py
   ```

## Команды бота

| Команда | Описание |
|---|---|
| `/start` | Главное меню |
| `/lessons` | Список модулей курса |
| `/tools` | Каталог ИИ-инструментов |
| `/tips` | Советы по промптингу |
| `/quiz` | Запустить квиз |
| `/help` | Справка |

## Технологии

- Python 3.10+
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) v21
- python-dotenv

## Лицензия

MIT
