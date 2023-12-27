import random
import discord
import aiohttp
from urllib.parse import urlencode
from discord import Embed
import json


async def hello(interaction: discord.Interaction):
    """Says hello!"""
    await interaction.response.send_message(f'Hi, {interaction.user.mention}')


async def books(interaction: discord.Interaction, baseurl: str, auth_header: dict):
    async with aiohttp.ClientSession() as session:
        async with session.get(baseurl + "/books", headers=auth_header) as response:
            if response.status == 200:
                data = await response.json()
                await interaction.response.send_message(f"Books data: {data}")
            else:
                print(f"Failed to retrieve data: {response.status}")
                await interaction.response.send_message("Failed to retrieve books data.")


async def roll(interaction: discord.Interaction, dice: str):
    try:
        dice = dice.lower().replace(' ', '')

        with open("roll_messages.json", "r") as file:
            quip_messages = json.load(file)

        allowed_dice = {'d4', 'd6', 'd8', 'd10', 'd12', 'd20', 'd100'}

        if 'd' not in dice or not any(d in dice for d in allowed_dice):
            await interaction.response.send_message('Allowed dice are d4, d6, d8, d10, d12, d20, and d100.')
            return

        parts = dice.split('d')
        num_rolls = int(parts[0]) if parts[0] else 1

        modifier = 0
        if '+' in parts[1]:
            limit_and_modifier = parts[1].split('+')
            limit = int(limit_and_modifier[0])
            modifier = int(limit_and_modifier[1])
        elif '-' in parts[1]:
            limit_and_modifier = parts[1].split('-')
            limit = int(limit_and_modifier[0])
            modifier = -int(limit_and_modifier[1])
        else:
            limit = int(parts[1])

        dice_type = f'd{limit}'
        if dice_type not in allowed_dice:
            await interaction.response.send_message(f'Invalid dice type! Allowed dice are {", ".join(allowed_dice)}.')
            return

        results = [random.randint(1, limit) for _ in range(num_rolls)]

        result_lines = []
        for result in results:
            modified_result = result + modifier
            if result == 20 and dice_type == 'd20':
                critical_message = "**Natural 20!! " + random.choice(
                    quip_messages["success"]) + '\n' + "**"

            elif result == 1 and dice_type == 'd20':
                critical_message = "**Natural 1. " + random.choice(
                    quip_messages["failure"]) + '\n' + "**"
            else:
                critical_message = ''

            result_lines.append(
                f"{critical_message} {result} (+{modifier}) = {modified_result} ")

        result_string = '\n'.join(result_lines)
        await interaction.response.send_message(result_string)
    except ValueError:
        await interaction.response.send_message('Invalid format or numbers!')
        return
    except Exception as e:
        await interaction.response.send_message(f'An unexpected error occurred: {e}')
        return


async def search(interaction: discord.Interaction, baseurl: str, auth_header: dict,
                 query: str, page: int = 1, count: int = 10):
    page = max(1, page)
    count = max(1, min(100, count))

    query_params = {
        'query': query,
        'page': page,
        'count': count
    }

    encoded_query = urlencode(query_params)
    search_url = f"{baseurl}/search?{encoded_query}"
    async with aiohttp.ClientSession() as session:
        async with session.get(search_url, headers=auth_header) as response:
            if response.status == 200:
                data = await response.json()

                if data['total'] > 0:
                    print(data)
                    embeds = []
                    for result in data['data']:
                        preview_content = result['preview_html']['content']
                        preview_content = preview_content.replace(
                            '<strong>', '**').replace('</strong>', '**')
                        preview_content = preview_content.replace(
                            '<u>', '__').replace('</u>', '__')

                        embed = Embed(
                            title=result['name'],
                            url=result['url'],
                            color=0x008080
                        )
                        if preview_content:
                            embed.add_field(
                                name="", value=preview_content, inline=False)
                        embeds.append(embed)
                    await interaction.response.send_message(embeds=embeds[:10])
                else:
                    await interaction.response.send_message("No results found.")
