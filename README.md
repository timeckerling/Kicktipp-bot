# Discord KickTipp Bot

A Discord bot made for the Allsvenskan-discord server that sends reminders for upcoming KickTipp match rounds. The bot checks a fixtures.json file and sends notifications to a specified Discord channel when matches are scheduled for the current day.

## Features

- Automatically sends reminders for matches scheduled on the current day
- Mentions users with a specific role to notify them about upcoming KickTipp deadlines
- Command `!next_game` to check when the next match is scheduled (currently not in active use)
- Simple test command `!test` for verifying the bot is working

## Prerequisites

- Python 3.8 or higher
- A Discord bot token (from [Discord Developer Portal](https://discord.com/developers/applications))
- A Discord server with a channel for notifications

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Environment Configuration

Create a `.env` file in the project root directory with the following variables:

```
DISCORD_TOKEN=your_discord_bot_token
CHANNEL_ID=your_discord_channel_id
KICKTIPP_URL=your_kicktipp_community_url
KICKTIPP_ROLE_ID=your_discord_role_id
```

### 4. AWS Deployment

1. Set up an EC2 instance or Lambda function
2. Install Python and required dependencies
3. Copy the project files to your AWS environment

#### Setting up a Cron Job on EC2

```bash
# Edit crontab
crontab -e

# Add a cron job to run daily at 8:00 AM (adjust time as needed)
0 8 * * * cd /path/to/project && python main.py
```

#### Troubleshooting Cron

If your cron job isn't running:

- Ensure cron service is running: `sudo service cron status`
- Check cron logs: `grep CRON /var/log/syslog`
- Verify Python path: `which python`
- Add absolute paths to your cron command
- Redirect output for debugging:
  ```
  0 8 * * * cd /path/to/project && python main.py >> /path/to/logfile.log 2>&1
  ```

## How It Works

1. The bot loads match fixtures from `fixtures.json`
2. It checks if any matches are scheduled for the current day
3. For each match found, it sends a reminder message to the configured Discord channel
4. The message includes:
   - A mention for users with the KickTipp role
   - The KickTipp URL
   - The deadline for submitting predictions
   - A friendly closing message

## File Structure

```
/
├── .env                # Environment variables (create this file)
├── fixtures.json       # Match schedule data
├── main.py             # Main bot code
└── README.md           # This documentation
```

## Customization

### Changing the Reminder Message

Edit the `send_reminder` function in `main.py` to customize the reminder message:

```python
reminder_message = (
    f'Snart dags att lämna in dina <@&{KICKTIPP_ROLE_ID}> resultat! \n \n'
    f'{KICKTIPP_URL} \n \n'
    f'Denna omgång har deadline idag {formatted_time} \n \n'
    f'Skål och lycka till!'
)
```

### Adding New Commands

To add new commands, use the `@client.command()` decorator:

```python
@client.command()
async def your_command_name(ctx):
    # Your command logic here
    await ctx.send("Your response")
```

## Maintenance

- Update the `fixtures.json` file when new fixtures are announced
- Keep your Discord bot token secure
- Monitor AWS resources and logs

## Security Considerations

- Never commit your `.env` file to version control
- Use AWS IAM roles with least privilege
- Consider using AWS Secrets Manager for sensitive information
