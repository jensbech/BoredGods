import discord
from bookstackapi import BookStackAPI
import aiohttp
from urllib.parse import urlencode
import os


client = BookStackAPI(intents=discord.Intents.default())

baseurl = os.getenv("BASE_URL")


@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')


@client.tree.command()
async def hello(interaction: discord.Interaction):
    """Says hello!"""
    await interaction.response.send_message(f'Hi, {interaction.user.mention}')


@client.tree.command()
async def books(interaction: discord.Interaction):
    async with aiohttp.ClientSession() as session:
        async with session.get(baseurl + "/books", headers=client.auth_header) as response:
            if response.status == 200:
                data = await response.json()

                await interaction.response.send_message(f"Books data: {data}")
            else:
                print(f"Failed to retrieve data: {response.status}")
                await interaction.response.send_message("Failed to retrieve books data.")


@client.tree.command()
async def search(interaction: discord.Interaction, query: str, page: int = 1, count: int = 10):
    page = max(1, page)
    count = max(1, min(100, count))

    query_params = {
        'query': query,
        'page': page,
        'count': count
    }

    encoded_query = urlencode(query_params)
    search_url = f"{baseurl}/search?{encoded_query}"
    print("Searching with url: " + search_url)
    async with aiohttp.ClientSession() as session:
        async with session.get(search_url, headers=client.auth_header) as response:
            if response.status == 200:
                data = await response.json()

                if data['total'] > 0:
                    await interaction.response.send_message(f"Search data: {data}")
                else:
                    await interaction.response.send_message("Alas, no results were found.")
            else:
                print(f"Failed to retrieve data: {response.status}")
                await interaction.response.send_message("Failed to retrieve search data.")


# The rename decorator allows us to change the display of the parameter on Discord.
# In this example, even though we use `text_to_send` in the code, the client will use `text` instead.
# Note that other decorators will still refer to it as `text_to_send` in the code.
# @client.tree.command()
# @app_commands.rename(text_to_send='text')
# @app_commands.describe(text_to_send='Text to send in the current channel')
# async def send(interaction: discord.Interaction, text_to_send: str):
#     """Sends the text into the current channel."""
#     await interaction.response.send_message(text_to_send)


# # To make an argument optional, you can either give it a supported default argument
# # or you can mark it as Optional from the typing standard library. This example does both.
# @client.tree.command()
# @app_commands.describe(member='The member you want to get the joined date from; defaults to the user who uses the command')
# async def joined(interaction: discord.Interaction, member: Optional[discord.Member] = None):
#     """Says when a member joined."""
#     # If no member is explicitly provided then we use the command user here
#     member = member or interaction.user

#     # The format_dt function formats the date time into a human readable representation in the official client
#     await interaction.response.send_message(f'{member} joined {discord.utils.format_dt(member.joined_at)}')


# # A Context Menu command is an app command that can be run on a member or on a message by
# # accessing a menu within the client, usually via right clicking.
# # It always takes an interaction as its first parameter and a Member or Message as its second parameter.

# # This context menu command only works on members
# @client.tree.context_menu(name='Show Join Date')
# async def show_join_date(interaction: discord.Interaction, member: discord.Member):
#     # The format_dt function formats the date time into a human readable representation in the official client
#     await interaction.response.send_message(f'{member} joined at {discord.utils.format_dt(member.joined_at)}')


# # This context menu command only works on messages
# @client.tree.context_menu(name='Report to Moderators')
# async def report_message(interaction: discord.Interaction, message: discord.Message):
#     # We're sending this response message with ephemeral=True, so only the command executor can see it
#     await interaction.response.send_message(
#         f'Thanks for reporting this message by {message.author.mention} to our moderators.', ephemeral=True
#     )

#     # Handle report by sending it into a log channel
#     log_channel = interaction.guild.get_channel(
#         0)  # replace with your channel id

#     embed = discord.Embed(title='Reported Message')
#     if message.content:
#         embed.description = message.content

#     embed.set_author(name=message.author.display_name,
#                      icon_url=message.author.display_avatar.url)
#     embed.timestamp = message.created_at

#     url_view = discord.ui.View()
#     url_view.add_item(discord.ui.Button(label='Go to Message',
#                       style=discord.ButtonStyle.url, url=message.jump_url))

#     await log_channel.send(embed=embed, view=url_view)


client.run(
    client.discord_token)
