from discord.ext import commands
from typing import Optional
import discord
from bookstack.apiclient import BookStackAPIClient
import os
from commands.roll import roll
from commands.search import search
import aiohttp
client = BookStackAPIClient(intents=discord.Intents.default())
baseurl = os.getenv("BASE_URL")


@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')


@client.tree.command(name="search")
async def search_command(interaction: discord.Interaction, query: str, page: int = 1, count: int = 10):
    await search(interaction, baseurl, client.auth_header, query, page, count)


@client.tree.command(name="roll")
async def roll_command(interaction: discord.Interaction, dice: str):
    await roll(interaction, dice)


CATEGORIES = ["spells", "weapons"]  # Add more item types as needed


@client.tree.command(name="rules")
async def lookup_command(
    interaction: discord.Interaction,
    spells: Optional[str] = None,
    weapons: Optional[str] = None,
    monsters: Optional[str] = None,
    equipment: Optional[str] = None,
    classes: Optional[str] = None
):
    query_param = [spells, weapons, monsters, equipment, classes]

    if spells not in CATEGORIES:
        error_message = f"Invalid item type. Please use from {
            ', '.join(CATEGORIES)}."
        await interaction.response.send_message(error_message)
        return

    if not spells:
        error_message = "Please provide the name of the item you want to look up."
        await interaction.response.send_message(error_message)
        return

    print("user sent item: ", spells)

    url = f"https://www.dnd5eapi.co/api/{item}/{item.value}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                await interaction.response.send_message(str(data))
            else:
                error_message = "Item not found or an error occurred. Please check the item name and try again."
                await interaction.response.send_message(error_message)

# Run the bot with the Discord token
client.run(os.getenv("DISCORD_TOKEN"))
