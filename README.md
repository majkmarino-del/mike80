# 🎬 AI Video School Bot

Telegram-бот для обучения созданию видео с помощью искусственного интеллекта.

## Что внутри

- 📚 **5 модулей обучения** — от основ до продвинутых техник
- 🛠 **Каталог ИИ-инструментов** — Sora, Veo, Seedance, Grok, Runway, Pika, Kling, HeyGen, ElevenLabs, Suno и др.
- ❓ **Квизы** для проверки знаний после каждого модуля
- 💡 **Советы по промптингу** для генерации видео
- 🚀 **Готовые рецепты** под разные задачи (Reels, YouTube Shorts, рекламные ролики)
- 🔒 **Доступ только по подписке на канал** — бот не отдаёт материал, пока пользователь не подписан

## Структура проекта

```
mike80/
├── main.py                    # Точка входа
├── requirements.txt
├── .env.example
└── bot/
    ├── config.py              # Загрузка переменных окружения
    ├── middleware.py          # Гейт подписки на канал
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

## 🚀 Быстрый запуск

### 1. Создайте бота в Telegram

1. Откройте [@BotFather](https://t.me/BotFather)
2. Команда `/newbot`, придумайте имя и username (должен заканчиваться на `bot`)
3. Скопируйте полученный **токен** (`123456:ABC-DEF...`)

### 2. Подготовьте канал-обязательную подписку

1. Создайте канал в Telegram (или используйте существующий).
2. Добавьте вашего бота **в администраторы** канала (можно без прав постить —
   достаточно базовых, главное чтобы бот был участником канала).
3. Зафиксируйте `@username` канала. Если канал приватный —
   запомните его invite-ссылку и числовой ID (`-100…`).

### 3. Установите зависимости и запустите

```bash
git clone https://github.com/majkmarino-del/mike80.git
cd mike80
python3 -m venv .venv
source .venv/bin/activate         # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

Откройте `.env` и заполните:

```dotenv
BOT_TOKEN=123456:ABC-DEF...
REQUIRED_CHANNEL=@my_ai_video_channel
# для приватных каналов:
# REQUIRED_CHANNEL=-1001234567890
# REQUIRED_CHANNEL_URL=https://t.me/+abcDEFghi
```

Запустите:

```bash
python main.py
```

В логах должно появиться:

```
Запускаю AI Video School Bot... required_channel=@my_ai_video_channel
```

Откройте чат с ботом, нажмите `/start` — должен появиться экран с просьбой
подписаться. После подписки нажмите «✅ Я подписался — проверить» — откроется главное меню.

## Команды бота

| Команда | Описание |
|---|---|
| `/start` | Главное меню |
| `/lessons` | Список модулей курса |
| `/tools` | Каталог ИИ-инструментов |
| `/tips` | Советы по промптингу |
| `/quiz` | Запустить квиз |
| `/help` | Справка |

## Как работает гейт подписки

- Перед каждым ответом бот вызывает `getChatMember(REQUIRED_CHANNEL, user_id)`.
- Если статус не `member`/`administrator`/`creator` — пользователь видит экран с
  кнопками «Перейти к каналу» и «Я подписался — проверить».
- Дальнейшая обработка останавливается (`ApplicationHandlerStop`).
- **Бот должен быть участником/админом канала**, иначе Telegram не разрешит ему
  читать список участников и каждый юзер будет видеть гейт.

## Технологии

- Python 3.10+
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) v21
- python-dotenv

## Лицензия

MIT
