class BotManager:

    def __init__(self, bot):
        self.bot = bot
    
    def on_irc_join(self):
        print("Connected to IRC.")
