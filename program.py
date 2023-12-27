import discord
from bookstack.apiclient import BookStackAPIClient
import os

from commands.roll import roll
from commands.search import search
from commands.weather import weather

client = BookStackAPIClient(intents=discord.Intents.default())
baseurl = os.getenv("BASE_URL")


@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')


@client.tree.command(name="søk")
async def search_command(interaction: discord.Interaction, query: str, page: int = 1, count: int = 10):
    await search(interaction, baseurl, client.auth_header, query, page, count)


@client.tree.command(name="terning")
async def roll_command(interaction: discord.Interaction, dice: str):
    await roll(interaction, dice)


@client.tree.command(name="værmelding")
async def weather_command(interaction: discord.Interaction):
    await weather(interaction)


@client.tree.command(name="hjelp")
async def help_command(interaction: discord.Interaction):
    messages = [
        "Følgende kommandoer er tilgjengelige:",
        "`/søk soskni` - Søk i Wiki",
        "`/rull d20` / `/rull 2d6-2` - Rull to win",
        "`/vær` - Sjekk været i Stone-upon-hill",
    ]
    help_message = "\n".join(messages)
    await interaction.response.send_message(help_message)

client.run(os.getenv("DISCORD_TOKEN"))
