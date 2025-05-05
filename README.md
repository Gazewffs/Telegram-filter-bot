# Telegram Channel Message Editor Bot

This bot monitors Telegram channels and automatically edits messages by applying text filters and converting timestamps between timezones.

## Features

- Monitor multiple Telegram channels
- Apply regex-based text filters to messages and captions
- Convert timestamps between timezones
- Easy configuration via Telegram commands
- Standalone operation without a web interface

## Setup on Termux

### Prerequisites

1. Install Termux from [F-Droid](https://f-droid.org/packages/com.termux/)
2. Create a Telegram bot using [@BotFather](https://t.me/botfather) and get your bot token

### Installation Steps

1. Update Termux packages:
   ```bash
   pkg update && pkg upgrade
   ```

2. Install required packages:
   ```bash
   pkg install python git
   ```

3. Clone or download the bot files to your Termux:
   ```bash
   # Create a directory for the bot
   mkdir -p ~/telegram-editor-bot
   
   # Extract the provided zip file or copy files to this directory
   cd ~/telegram-editor-bot
   # Extract zip file if provided
   # unzip telegram-editor-bot.zip
   ```

4. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Set up your bot token:
   ```bash
   # Add your Telegram bot token to environment
   echo "export TELEGRAM_BOT_TOKEN='your_bot_token_here'" >> ~/.bashrc
   source ~/.bashrc
   ```

6. Configure your timezones (optional):
   Edit `config.py` to set your preferred source and target timezones.
   ```python
   # Default source timezone (where messages come from)
   SOURCE_TIMEZONE = "Etc/GMT-14"
   
   # Default target timezone (where you want times converted to)
   TARGET_TIMEZONE = "Asia/Kolkata"
   ```

7. Run the bot:
   ```bash
   python main.py
   ```

8. To run the bot in the background (even when Termux is closed):
   ```bash
   nohup python main.py > bot.log 2>&1 &
   ```

### Running with VPS Manager (Hostinger)

If you're using a VPS from Hostinger:

1. Connect to your VPS using SSH
2. Follow the same installation steps as above
3. To keep the bot running after you disconnect:
   ```bash
   # Install screen if not already installed
   apt-get install screen
   
   # Create a new screen session
   screen -S telegram-bot
   
   # Run your bot
   cd ~/telegram-editor-bot
   python main.py
   
   # Detach from screen by pressing Ctrl+A then D
   ```

4. To reattach to your bot screen later:
   ```bash
   screen -r telegram-bot
   ```

## Bot Commands

Once your bot is running, you can control it with these Telegram commands:

- `/start` - Start the bot and get a welcome message
- `/help` - Show all available commands and usage information
- `/status` - Check the bot's current status
- `/channels` - List all monitored channels
- `/addchannel @channel_name` - Add a channel to monitor
- `/removechannel @channel_name` - Remove a channel from monitoring
- `/filters` - List all active text filters
- `/addfilter pattern replacement` - Add a new text filter
- `/removefilter pattern` - Remove a text filter
- `/testfilter "sample text" pattern` - Test a regex pattern on sample text

## Adding Your Bot to a Channel

1. Add your bot as an administrator to your Telegram channel
2. Give it permission to post and edit messages
3. Send `/addchannel @your_channel_name` to your bot in a direct message
4. The bot will now monitor and edit messages in that channel

## Customizing Text Filters

You can add text filters using regex patterns. For example:

- `/addfilter "(?i)\\b(urgent)\\b" "URGENT"` - Replace "urgent" with "URGENT" (case insensitive)

The bot also includes some pre-configured filters in `config.py` that you can modify.

## Troubleshooting

- Check the `bot.log` file for errors
- Make sure your bot has admin permissions in the channel
- Verify your bot token is set correctly
- Ensure the timezones in `config.py` are valid

## Keeping the Bot Running

To ensure the bot stays running even if your phone restarts, you can set up a simple startup script:

1. Create a startup script:
   ```bash
   echo '#!/data/data/com.termux/files/usr/bin/bash
   cd ~/telegram-editor-bot
   nohup python main.py > bot.log 2>&1 &' > ~/start-bot.sh
   
   chmod +x ~/start-bot.sh
   ```

2. Add it to your Termux startup:
   ```bash
   mkdir -p ~/.termux/boot
   ln -s ~/start-bot.sh ~/.termux/boot/
   ```

3. Enable Termux boot service by installing the Termux:Boot app from F-Droid.

## Updating the Bot

To update the bot in the future:

1. Stop the current bot process
2. Back up your config files and JSON data
3. Replace the code files with the new ones
4. Restore your config files if needed
5. Restart the bot

## Support

If you encounter any issues, please check the logs first and then seek help from the developer.