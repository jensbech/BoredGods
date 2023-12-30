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

        result_lines = generate_results(
            results, limit, modifier, quip_messages, interaction.user.name)

        result_string = '\n'.join(result_lines)
        await interaction.response.send_message(content=result_string)

    except ValueError as e:
        await interaction.response.send_message(f'Invalid format or numbers! {e}')
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


def generate_results(results, limit, modifier, quip_messages, user_name):
    result_lines = []
    for result in results:
        critical_message = get_critical_message(result, limit, quip_messages)
        modified_result = result + modifier

        result_line = generate_result_line(
            result, modifier, modified_result, critical_message)

        result_lines.append(result_line)

        if result == 20 and limit == 20:
            result_lines.append(set_critical_song(user_name))
    return result_lines


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


def set_critical_song(user_name):
    with open("resources/critical_songs.json", "r") as file:
        song_dict = json.load(file)

    default_song_link = "https://open.spotify.com/track/7yU7FlMnnLHEnOVxMmQLCQ?si=3f3693f8cef847ef"
    song_link = song_dict.get(user_name, default_song_link)

    return song_link
