import json
import discord
import random


async def roll(interaction: discord.Interaction, dice: str):
    try:
        dice = dice.lower().replace(' ', '')

        with open("resources/dice_critical_responses.json", "r") as file:
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
        embeds = []

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

            if modifier == 0:
                result_lines.append(
                    f"{critical_message} {modified_result} "
                )
            else:
                result_lines.append(
                    f"{critical_message} {
                        result} (+{modifier}) = {modified_result} "
                )

            if result == 20 and dice_type == 'd20':
                spotifySongEmbed = discord.Embed(
                    title="Nina Sublatti",
                    description="Warrior",
                    url="https://open.spotify.com/track/7yU7FlMnnLHEnOVxMmQLCQ?si=3f3693f8cef847ef",
                    color=0x1DB954)

                spotifySongEmbed.set_thumbnail(
                    url="https://i1.sndcdn.com/artworks-000122405931-31a939-t500x500.jpg")
                embeds.append(spotifySongEmbed)

        result_string = '\n'.join(result_lines)
        await interaction.response.send_message(content=result_string, embeds=embeds)

    except ValueError:
        await interaction.response.send_message('Invalid format or numbers!')
        return
    except Exception as e:
        await interaction.response.send_message(f'An unexpected error occurred: {e}')
        return
