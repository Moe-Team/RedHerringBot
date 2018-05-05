class BotManager:

    def __init__(self, bot):
        self.bot = bot
    
    def on_irc_join(self):
        await bot.say("Connected to IRC.")
