import logging
import os
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Telegram bot token from environment variable
TOKEN = 7583810398:AAG41wb6YdM9FgPfLEY58PttP8P_dgPtOWU

# Поддерживаемые монеты
COINS = {
    "xrp": "ripple",
    "hbar": "hedera-hashgraph",
    "grt": "the-graph",
    "pepe": "pepe",
    "goar": "goar"  # ⚠️ если coin не существует на CoinGecko — заменить
}

# Логгинг
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def get_price_data(coin_id):
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}"
    res = requests.get(url)
    if res.status_code == 200:
        data = res.json()
        return {
            "name": data["name"],
            "price": data["market_data"]["current_price"]["usd"],
            "market_cap": data["market_data"]["market_cap"]["usd"],
            "change_24h": data["market_data"]["price_change_percentage_24h"]
        }
    else:
        return None

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Привет! Я крипто-бот.\nНапиши команду:\n/analyze xrp")

def analyze(update: Update, context: CallbackContext):
    if len(context.args) == 0:
        update.message.reply_text("Укажи тикер монеты: /analyze xrp")
        return

    symbol = context.args[0].lower()
    if symbol not in COINS:
        update.message.reply_text("Эта монета не поддерживается.")
        return

    data = get_price_data(COINS[symbol])
    if data:
        reply = f"📊 *{data['name']}*\n" \
                f"💰 Цена: ${data['price']:.4f}\n" \
                f"📉 24ч Изм: {data['change_24h']:.2f}%\n" \
                f"🏦 Капитализация: ${data['market_cap']:,}"
        update.message.reply_text(reply, parse_mode="Markdown")
    else:
        update.message.reply_text("Не удалось получить данные.")

def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("analyze", analyze))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
