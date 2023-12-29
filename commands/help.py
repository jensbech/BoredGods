import discord


async def help(interaction: discord.Interaction):
    messages = [
        "Følgende kommandoer er tilgjengelige:",
        "`/søk <query>` - Søk i Wiki",
        "`/terning <dice>` - Rull terning",
        "`/værmelding` - Sjekk været i Stone-upon-hill",
    ]
    help_message = "\n".join(messages)
    await interaction.response.send_message(help_message)
