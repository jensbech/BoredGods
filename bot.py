from discord.ext import commands
from dotenv import load_dotenv
import aiohttp
import os


load_dotenv()


class BookStackAPI(commands.Cog):
    def __init__(self, bot, base_url):
        self.bot = bot
        self.base_url = base_url
        self.api_id = os.getenv('BOOKSTACK_API_ID')
        self.api_key = os.getenv('BOOKSTACK_API_KEY')
        self.auth_header = {'Authorization': f'Token {
            self.api_id}:{self.api_key}'
        }

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Logged in as {self.bot.user.name}')

    @commands.command(name="books", description="Retrieve books data")
    async def books(self, ctx: commands.context):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.base_url + "/books", headers=self.auth_header) as response:
                if response.status == 200:
                    data = await response.json()
                    await ctx.send(f"Books data: {data}")
                else:
                    print(f"Failed to retrieve data: {response.status}")
                    await ctx.send("Failed to retrieve books data.")

    @commands.command()
    async def search(self, ctx: commands.context, query: str):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.base_url + f"/search?query={query}", headers=self.auth_header) as response:
                if response.status == 200:
                    data = await response.json()
                    await ctx.send(f"Search data: {data}")
                else:
                    print(f"Failed to retrieve data: {response.status}")
                    await ctx.send("Failed to retrieve search data.")
