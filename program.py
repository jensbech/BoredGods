import discord
from discord.ext import commands
import os
from bot import BookStackAPI
import asyncio


def custom_prefix(bot, message):
    return commands.when_mentioned_or()(bot, message)


async def main():
    intents = discord.Intents.all()
    bot = commands.Bot(command_prefix=custom_prefix, intents=intents)

    await bot.add_cog(BookStackAPI(bot, "https://wiki.boredgods.no/api"))

    await bot.start(os.getenv('BOT_TOKEN'))

asyncio.run(main())
