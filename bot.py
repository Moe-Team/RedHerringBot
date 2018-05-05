import discord
from discord.ext import commands
import aiohttp
import threading
import time
from bot_irc import create_irc_connection, create_own_connection
from bot_manager import BotManager

description = """Work in progress."""


bot = commands.Bot(command_prefix='r!', description=description)


@bot.event
async def on_ready():
    print("Logged in.")


@bot.event
async def on_message(message):
    await bot.process_commands(message)


@bot.command(pass_context=True)
async def change_avatar(ctx, url: str):
    if ctx.message.author.id != '178887072864665600':
        await bot.say("You're not Zack enough.")
        return
    with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            avatar_b = await resp.read()
            await bot.edit_profile(avatar=avatar_b)


@bot.command(pass_context=True)
async def dismiss(ctx):
    """Put the bot to sleep."""
    if ctx.message.author.id == '178887072864665600':
        await bot.say("Going to sleep.")
        await bot.logout()
    else:
        await bot.say("You wish.")
        return


@bot.command(pass_context=True)
async def debug(ctx, *args):
    if ctx.message.author.id != '178887072864665600':
        await bot.say("No.")
        return
    command = ' '.join(args)
    # Do not do this at home kids
    exec(command, globals(), locals())


@bot.command(pass_context=True)
async def create_irc(ctx, server: str, port: int, username: str):
    bot_manager = BotManager(bot)
    irc_connection = create_own_connection(server, port, username)
    def test_irc(*args):
        while True:
            irc_connection.process()
    threading.Thread(target=test_irc, args=(irc_connection,)).start()
