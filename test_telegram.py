from telegram import Bot

def test_telegram():
    try:
        bot = Bot(token="7987369503:AAFctUC3qE0cP0zQQrL8GHYvcvc9IlYYzUQ")
        bot.send_message(chat_id="5560117568", text="✅ Token works!")
        print("✅ Telegram test successful!")
    except Exception as e:
        print(f"❌ Telegram test failed: {e}")

if __name__ == "__main__":
    test_telegram() 