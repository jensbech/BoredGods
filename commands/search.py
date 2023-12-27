import aiohttp
from urllib.parse import urlencode
from discord import Embed
import discord


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
