import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import aiohttp

load_dotenv()


class DiscordBot:
    def __init__(self, command_prefix, intents):
        self.bot = commands.Bot(command_prefix=command_prefix, intents=intents)

    async def on_ready(self):
        print(f'Logged in as {self.bot.user.name}')

    async def get_data_from_api(self):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://wiki.boredgods.no/api/books') as response:
                if response.status == 200:
                    data = await response.json()
                    return data
                else:
                    print(f"Failed to retrieve data: {response.status}")
                    return None

    @commands.command(name='getbooks')  # Define the command
    async def get_books(self, ctx):
        print("get_books called")
        data = await self.get_data_from_api()
        if data:
            await ctx.send(f"Books data: {data}")
        else:
            await ctx.send("Failed to retrieve books data.")

    def run(self):
        self.bot.add_command(self.get_books)

        @self.bot.event
        async def on_ready():
            await self.on_ready()

        self.bot.run(os.getenv('BOT_TOKEN'))


if __name__ == "__main__":
    intents = discord.Intents.all()
    my_bot = DiscordBot(command_prefix='/', intents=intents)
    my_bot.run()
