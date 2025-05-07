import os
from telegram import Bot
from strategy import analyze_symbol

# Telegram configuration
BOT_TOKEN = "7987369503:AAFctUC3qE0cP0zQQrL8GHYvcvc9IlYYzUQ"
CHAT_ID = "5560117568"

# Initialize bot
bot = Bot(token=BOT_TOKEN)

# Test bot token
try:
    bot.send_message(chat_id=CHAT_ID, text="✅ Testing bot token")
    print("✅ Telegram bot token is valid")
except Exception as e:
    print(f"❌ Telegram failed: {e}")
    exit(1)  # Exit if token is invalid

# Trading symbols
symbols = {
    'NAS100': 'NAS100',
    'XAUUSD': 'XAUUSD',
    'GBPUSD': 'GBPUSD'
}

def send_signal(name, signal, chart_path):
    try:
        bot.send_message(chat_id=CHAT_ID, text=signal, parse_mode="Markdown")
        if chart_path:
            with open(chart_path, "rb") as image:
                bot.send_photo(chat_id=CHAT_ID, photo=image)
    except Exception as e:
        print(f"❌ Error sending Telegram message for {name}: {e}")

def main():
    for name, ticker in symbols.items():
        print(f"Analyzing {name}...")
        signal, chart_path = analyze_symbol(name, ticker)
        
        if chart_path is None:
            print(f"⚠️ Skipping {name} due to missing data or chart.")
            continue

        send_signal(name, signal, chart_path)

if __name__ == "__main__":
    main()
