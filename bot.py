import os
import threading
import telebot
from openai import OpenAI
from flask import Flask

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        response = client.chat.completions.create(
    model="google/gemini-2.5-flash",
    messages=[
        {"role": "system", "content": "Ты — дружелюбный помощник. Отвечай на русском языке."},
        {"role": "user", "content": message.text}
    ],
    max_tokens=500
        )
        bot.reply_to(message, response.choices[0].message.content)
    except Exception as e:
        bot.reply_to(message, f"Ошибка: {e}")

app = Flask(__name__)

@app.route('/')
def home():
    return "Бот работает!"

@app.route('/health')
def health():
    return "OK", 200

def run_bot():
    print("✅ Бот запущен!")
    bot.infinity_polling()

if __name__ == '__main__':
    thread = threading.Thread(target=run_bot)
    thread.start()
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
