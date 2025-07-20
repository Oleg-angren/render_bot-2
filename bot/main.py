import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from flask import Flask, request

# === Настройки бота ===
BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # Например: https://your-bot.onrender.com 
PORT = int(os.getenv("PORT", 10000))  # Render передаёт PORT

# === Инициализация бота и Flask сервера ===
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

app = Flask(__name__)

# === Обработчики бота ===
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.answer("Привет! Я бот на webhook.")

@dp.message_handler()
async def echo_message(message: types.Message):
    await message.answer(message.text)

# === Webhook endpoint ===
@app.route(f'/{BOT_TOKEN}', methods=['POST'])
async def webhook():
    update = types.Update(**request.get_json())
    await dp.process_update(update)
    return {"status": "ok"}

# === Домашняя страница (для Render и UptimeRobot) ===
@app.route('/')
def home():
    return "Бот работает!"

# === Установка webhook при запуске ===
async def on_startup():
    webhook_url = f"{WEBHOOK_URL}/{BOT_TOKEN}"
    await bot.set_webhook(webhook_url)
    print(f"Webhook установлен: {webhook_url}")

# === Запуск Flask и бота ===
def run():
    asyncio.run(on_startup())
    app.run(host='0.0.0.0', port=PORT)

if __name__ == '__main__':
    run()
