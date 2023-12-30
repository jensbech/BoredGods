import discord


async def help(interaction: discord.Interaction):
    messages = [
        "Available commands:",
        "`/search <query>` - Search the Bored Gods Wiki",
        "`/roll <dice>` - Roll some dice",
        "`/weather` - Check the Stone-upon-hill weather!",
        "`/chat <question>` - Ask about DND rules",
    ]
    help_message = "\n".join(messages)
    await interaction.response.send_message(help_message)
