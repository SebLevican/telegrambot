import os
from dotenv import load_dotenv
from telegram_bot import TelegramBot

load_dotenv()
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

if __name__ == '__main__':
    bot = TelegramBot(TELEGRAM_TOKEN)
    bot.run()
