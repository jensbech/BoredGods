import discord
from bookstack.apiclient import BookStackAPIClient
import os

from commands.roll import roll
from commands.search import search
from commands.weather import weather
from commands.help import help
from commands.chat import chat
from webhooks.new_post import create_app
import threading

discord_client = BookStackAPIClient(intents=discord.Intents.default())
baseurl = os.getenv("BASE_URL")


@discord_client.event
async def on_ready():
    print(f'Logged in as {discord_client.user} (ID: {discord_client.user.id})')


@discord_client.tree.command(name="søk")
async def search_command(interaction: discord.Interaction, query: str, page: int = 1, count: int = 10):
    await search(interaction, baseurl, discord_client.auth_header, query, page, count)


@discord_client.tree.command(name="terning")
async def roll_command(interaction: discord.Interaction, dice: str):
    await roll(interaction, dice)


@discord_client.tree.command(name="værmelding")
async def weather_command(interaction: discord.Interaction):
    await weather(interaction)


@discord_client.tree.command(name="hjelp")
async def help_command(interaction: discord.Interaction):
    await help(interaction)


@discord_client.tree.command(name="chat")
async def chat_command(interaction: discord.Interaction):
    await chat(interaction)


def run_flask_app():
    flask_app = create_app(discord_client)
    flask_app.run(host='0.0.0.0', port=5000)


if __name__ == '__main__':
    flask_thread = threading.Thread(target=run_flask_app)
    flask_thread.daemon = True
    flask_thread.start()

    discord_client.run(os.getenv("DISCORD_TOKEN"))
