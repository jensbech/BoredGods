from dotenv import load_dotenv
import o
from discord import app_commands


load_dotenv()


class BookStackAPI(commands.Cog):
    def __init__(self, bot, base_url):
        self.bot = bot
        self.base_url = base_url

        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        self.tree.copy_global_to(guild="1104114229931421786")
        await self.tree.sync(guild="1104114229931421786")

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
