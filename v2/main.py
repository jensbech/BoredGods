import discord
from bookstackapi import BookStackAPI
import os
from v2.user_commands import hello, books, search

client = BookStackAPI(intents=discord.Intents.default())
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

client.run(client.discord_token)
