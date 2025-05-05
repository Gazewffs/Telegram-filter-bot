#!/bin/bash

echo "===== Telegram Channel Message Editor Bot - Termux Installation ====="
echo ""

# Check if running in Termux
if [ ! -d "/data/data/com.termux" ]; then
    echo "Warning: This doesn't appear to be Termux. Installation may not work correctly."
    echo "Press Enter to continue anyway, or Ctrl+C to cancel."
    read
fi

# Update packages
echo "Updating Termux packages..."
pkg update -y

# Install required packages
echo "Installing required packages..."
pkg install -y python python-pip

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Set up environment
echo ""
echo "Setting up bot configuration..."

# Ask for bot token
echo ""
echo "Please enter your Telegram Bot Token (obtained from @BotFather):"
read -p "> " BOT_TOKEN

# Save the token to environment and .env file
echo "export TELEGRAM_BOT_TOKEN='$BOT_TOKEN'" >> ~/.bashrc
echo "TELEGRAM_BOT_TOKEN=$BOT_TOKEN" > .env

# Timezone configuration
echo ""
echo "Do you want to customize timezone settings? (y/n)"
read -p "> " CUSTOM_TZ

if [[ "$CUSTOM_TZ" == "y" || "$CUSTOM_TZ" == "Y" ]]; then
    echo "Enter source timezone (e.g., Etc/GMT-14, UTC, Europe/London):"
    read -p "> " SOURCE_TZ
    
    echo "Enter target timezone (e.g., Asia/Kolkata, America/New_York):"
    read -p "> " TARGET_TZ
    
    # Simple find and replace in config.py
    if [ ! -z "$SOURCE_TZ" ]; then
        sed -i "s/SOURCE_TIMEZONE = \".*\"/SOURCE_TIMEZONE = \"$SOURCE_TZ\"/" config.py
    fi
    
    if [ ! -z "$TARGET_TZ" ]; then
        sed -i "s/TARGET_TIMEZONE = \".*\"/TARGET_TIMEZONE = \"$TARGET_TZ\"/" config.py
    fi
    
    echo "Timezone settings updated in config.py"
fi

# Create startup script
echo ""
echo "Do you want to create a startup script for the bot? (y/n)"
read -p "> " CREATE_STARTUP

if [[ "$CREATE_STARTUP" == "y" || "$CREATE_STARTUP" == "Y" ]]; then
    echo '#!/data/data/com.termux/files/usr/bin/bash
cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source ~/.bashrc
nohup python main.py > bot.log 2>&1 &' > start-bot.sh
    
    chmod +x start-bot.sh
    
    echo "Created startup script: $(pwd)/start-bot.sh"
    echo ""
    echo "To have the bot start automatically, install Termux:Boot from F-Droid"
    echo "and link this script to ~/.termux/boot/"
fi

# Final instructions
echo ""
echo "===== Installation Complete ====="
echo ""
echo "To start the bot now, run:"
echo "  python main.py"
echo ""
echo "To run the bot in background:"
echo "  nohup python main.py > bot.log 2>&1 &"
echo ""
echo "See README.md for more information on bot usage and commands."
echo ""