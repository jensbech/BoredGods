import discord
from bookstack.apiclient import BookStackAPIClient
import os
from commands.roll import roll
from commands.search import search
import aiohttp
client = BookStackAPIClient(intents=discord.Intents.default())
baseurl = os.getenv("BASE_URL")

valid_categories = ["classes", "conditions",
                    "equipment", "feats",
                    "languages", "magic-items", "magic-schools", "monsters", "proficiencies",
                    "races", "skills",
                    "weapons", "spells"]


@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')


@client.tree.command(name="søk")
async def search_command(interaction: discord.Interaction, query: str, page: int = 1, count: int = 10):
    await search(interaction, baseurl, client.auth_header, query, page, count)


@client.tree.command(name="terning")
async def roll_command(interaction: discord.Interaction, dice: str):
    await roll(interaction, dice)


@client.tree.command(name="regler")
async def lookup_command(interaction: discord.Interaction, kategori: str, navn: str):

    if kategori not in valid_categories:
        error_message = f"Ukjent kategori. Bruk en av de følgende: **{
            ', '.join(valid_categories)}**."
        await interaction.response.send_message(error_message)
        return

    resolvedName = navn.replace(" ", "-").lower()

    url = f"https://www.dnd5eapi.co/api/{kategori}/{resolvedName}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()

                print(data)

                name = data['name']
                desc = data['desc'][0]

                message = f"\n**Name:** {name}\n"
                message += f"**Description:** {desc}"

                await interaction.response.send_message(message)
            else:
                error_message = "Regel ikke funnet, eller en feil. Sjekk navnet og prøv igjen!"
                await interaction.response.send_message(error_message)


@client.tree.command(name="hjelp")
async def help_command(interaction: discord.Interaction):
    category_list = ", ".join(
        [f"`{category}`" for category in valid_categories])

    messages = [
        "Følgende kommandoer er tilgjengelige:",
        "`/søk soskni` - Søk i Wiki",
        "`/rull d20`- Rull to win",
        "`/regler`",
        "\nTilgjengelige kategorier for `/regler <kategori> <navn>`:",
        category_list
    ]

    help_message = "\n".join(messages)
    await interaction.response.send_message(help_message)

client.run(os.getenv("DISCORD_TOKEN"))
