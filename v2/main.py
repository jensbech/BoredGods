import discord
from bookstackapi import BookStackAPIClient
import os
from user_commands import hello, books, search, roll

client = BookStackAPIClient(intents=discord.Intents.default())
baseurl = os.getenv("BASE_URL")


@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')


@client.tree.command(name="hello")
async def hello_command(interaction: discord.Interaction):
    await hello(interaction)


@client.tree.command(name="books")
async def books_command(interaction: discord.Interaction):
    await books(interaction, baseurl, client.auth_header)


@client.tree.command(name="search")
async def search_command(interaction: discord.Interaction, query: str, page: int = 1, count: int = 10):
    await search(interaction, baseurl, client.auth_header, query, page, count)


@client.tree.command(name="roll")
async def roll_command(interaction: discord.Interaction, dice: str, modifier: int = 0):
    await roll(interaction, dice)

client.run(client.discord_token)
