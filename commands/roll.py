import json
import discord
import random


async def roll(interaction: discord.Interaction, dice: str):
    try:
        dice = parse_dice_string(dice)
        if not dice:
            await interaction.response.send_message('Allowed dice are d4, d6, d8, d10, d12, d20, and d100.')
            return

        num_rolls, limit, modifier = extract_roll_parameters(dice)

        results = roll_dice(num_rolls, limit)

        quip_messages = load_quip_messages()
        result_lines, embeds = generate_results_and_embeds(
            results, limit, modifier, quip_messages)

        result_string = '\n'.join(result_lines)
        await interaction.response.send_message(content=result_string, embeds=embeds)

    except ValueError:
        await interaction.response.send_message('Invalid format or numbers!')
    except Exception as e:
        await interaction.response.send_message(f'An unexpected error occurred: {e}')


def parse_dice_string(dice_str):
    allowed_dice = {'d4', 'd6', 'd8', 'd10', 'd12', 'd20', 'd100'}
    dice_str = dice_str.lower().replace(' ', '')
    if 'd' not in dice_str or not any(d in dice_str for d in allowed_dice):
        return None
    return dice_str


def extract_roll_parameters(dice_str):
    parts = dice_str.split('d')
    num_rolls = int(parts[0]) if parts[0] else 1
    limit, modifier = parse_limit_and_modifier(parts[1])
    return num_rolls, limit, modifier


def parse_limit_and_modifier(part):
    if '+' in part:
        limit, modifier = map(int, part.split('+'))
    elif '-' in part:
        limit, modifier = part.split('-')
        limit = int(limit)
        modifier = -int(modifier)
    else:
        limit = int(part)
        modifier = 0
    return limit, modifier


def roll_dice(num_rolls, limit):
    return [random.randint(1, limit) for _ in range(num_rolls)]


def load_quip_messages():
    with open("resources/dice_critical_responses.json", "r") as file:
        return json.load(file)


def generate_results_and_embeds(results, limit, modifier, quip_messages):
    result_lines = []
    embeds = []
    for result in results:
        critical_message = get_critical_message(result, limit, quip_messages)
        modified_result = result + modifier
        result_line = generate_result_line(
            result, modifier, modified_result, critical_message)
        result_lines.append(result_line)
        if result == 20 and limit == 20:
            embeds.append(create_natural_20_embed())
    return result_lines, embeds


def get_critical_message(result, limit, quip_messages):
    if result == 20 and limit == 20:
        return f"**Natural 20!! {random.choice(quip_messages['success'])}\n**"
    elif result == 1 and limit == 20:
        return f"**Natural 1. {random.choice(quip_messages['failure'])}\n**"
    return ''


def generate_result_line(result, modifier, modified_result, critical_message):
    sign = "-" if modifier < 0 else "+"
    if modifier == 0:
        return f"{critical_message}{modified_result}"
    else:
        return f"{critical_message}{result} ({sign}{abs(modifier)}) = {modified_result}"


def create_natural_20_embed():
    thumb = discord.Embed(
        title="Nina Sublatti",
        description="Warrior",
        url="https://open.spotify.com/track/7yU7FlMnnLHEnOVxMmQLCQ?si=3f3693f8cef847ef",
        color=0x1DB954
    )
    thumb.set_thumbnail(
        url="https://wiki.boredgods.no/uploads/images/gallery/2023-12/thumbs-150-150/spotify-icon-svg.png"
    )
    return thumb
