import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

bot.run(os.getenv('BOT_TOKEN'))
