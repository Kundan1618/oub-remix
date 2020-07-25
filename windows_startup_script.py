from telethon import TelegramClient, events
API_KEY="Type that here"
API_HASH="Type that here"
#get it from my.telegram.org
bot = TelegramClient('userbot',API_KEY,API_HASH)
bot.alive()

#This script wont run your bot, it just generates a session.
