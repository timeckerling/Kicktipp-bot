import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from datetime import datetime, timezone
from dateutil import parser
import json
from pathlib import Path

# Environment setup
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))
TEST_CHANNEL_ID = int(os.getenv('TEST_CHANNEL_ID'))  # For debugging
KICKTIPP_URL = os.getenv('KICKTIPP_URL')
KICKTIPP_ROLE_ID = int(os.getenv('KICKTIPP_ROLE_ID'))


# Bot setup
intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='!', intents=intents)


# Load from json
def get_fixtures():
    fixture_path = Path('fixtures.json')
    try:
        return json.loads(fixture_path.read_text())
    except FileNotFoundError:
        print("fixtures.json file not found.")
        return None


# Get upcoming matches (Not in use)
def get_upcoming_matches():
    data = get_fixtures()
    if not data:
        return []

    matches = []
    now = datetime.now(timezone.utc)
    today = now.date()

    for round_data in data.get('rounds', []):
        match_datetime_str = f"{round_data['date']}T{round_data['time']}Z"
        try:
            match_time = parser.parse(
                match_datetime_str).astimezone(timezone.utc)
            if match_time.date() == today:
                matches.append({
                    'time': match_time,
                    'round': round_data['round'],
                    'start_time': match_time
                })
        except ValueError:
            print(f"Error parsing date: {match_datetime_str}")

    return matches


# Test message (Comment out if not needed)
# async def send_test_message():
#    await client.wait_until_ready()
#    if test_channel := client.get_channel(TEST_CHANNEL_ID):
#        test_message = f'Tjääääna! FalconBot här för att skicka ett testmeddelande, och påminna er om hur jävla fula djurgården är. \n \n Hare!'
#        await test_channel.send(test_message)
#        print(f"Sent test message to channel {TEST_CHANNEL_ID}")
#    else:
#        print(f"Error: Could not find test channel with ID {TEST_CHANNEL_ID}")


# Reminder message
async def send_reminder(match):
    await client.wait_until_ready()
    if channel := client.get_channel(CHANNEL_ID):
        formatted_time = match["start_time"].strftime("%Y-%m-%d %H:%M")
        reminder_message = (
            f'Snart dags att lämna in dina <@&{KICKTIPP_ROLE_ID}> resultat! \n \n'
            f'{KICKTIPP_URL} \n \n'
            f'Denna omgång har deadline idag {formatted_time} \n \n'
            f'Skål och lycka till!'
        )
        await channel.send(reminder_message)
        print(f"Sent reminder for round {match['round']}")
    else:
        print(f"Error: Could not find channel with ID {CHANNEL_ID}")


async def send_daily_reminders():
    if matches := get_upcoming_matches():
        for match in matches:
            await send_reminder(match)
            # await send_test_message()
    else:
        print("No matches today.")
        # await send_test_message()


def get_next_match_date():
    data = get_fixtures()
    if not data:
        return "Inga matcher hittades."

    now = datetime.now(timezone.utc)
    upcoming_matches = []

    for round_data in data.get('rounds', []):
        match_datetime_str = f"{round_data['date']}T{round_data['time']}Z"
        try:
            match_time = parser.parse(
                match_datetime_str).astimezone(timezone.utc)
            if match_time > now:
                upcoming_matches.append(match_time)
        except ValueError:
            print(f"Error parsing date: {match_datetime_str}")

    if upcoming_matches:
        next_match = min(upcoming_matches)
        return f"Nästa match är {next_match.strftime('%Y-%m-%d %H:%M')}"
    else:
        return "Ingen kommande match hittades."


# Next game command (Not in use)
@client.command()
async def next_game(ctx):
    message = get_next_match_date()
    await ctx.send(message)


# Login event handler
@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    if __name__ == "__main__":
        await send_daily_reminders()
        await client.close()  # Remove comment if you want to stay logged in


# Test command
@client.command()
async def test(ctx):
    await ctx.send("Djurgårn e fulast i stan!")


# Makes shit run
def run_bot():
    client.run(TOKEN)


if __name__ == "__main__":
    run_bot()
