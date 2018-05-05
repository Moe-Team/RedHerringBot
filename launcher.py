from bot import bot
import os
bot_token = os.environ['BOT_TOKEN']

bot.run(bot_token)
