import discord
from bot import DiscordBot

bot = DiscordBot(command_prefix='/', intents=discord.Intents.all())

bot.run()
