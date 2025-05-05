#!/usr/bin/env python3
"""
Test script for Telegram Channel Message Editor Bot.
This script tests the bot's functionality without actually connecting to Telegram.
"""

import logging
import re
import os
import json
from utils import process_message_text
from filter_manager import get_all_filters, list_filters
from config import SOURCE_TIMEZONE, TARGET_TIMEZONE

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

def test_filters():
    """Test that filters are working correctly"""
    print("\n=== Testing filters ===")
    
    # Get all configured filters
    filters = get_all_filters()
    print(f"Found {len(filters)} filters")
    
    # Display formatted list
    print("\nFilters list:")
    print(list_filters())
    
    # Test sample texts
    test_texts = [
        "This is URGENT and IMPORTANT",
        "Meeting at 18:50:00",
        "Contact @Gazew_07 for more info",
        "Project status: 🚧 In Progress 🚧"
    ]
    
    print("\nTesting sample messages:")
    for i, text in enumerate(test_texts, 1):
        print(f"\nTest {i}:\nOriginal: {text}")
        processed = process_message_text(text)
        print(f"Processed: {processed}")
        if text != processed:
            print("✅ Filter applied successfully")
        else:
            print("❌ No changes made")

def test_timezone_conversion():
    """Test that timezone conversion is working"""
    print("\n=== Testing timezone conversion ===")
    print(f"Source timezone: {SOURCE_TIMEZONE}")
    print(f"Target timezone: {TARGET_TIMEZONE}")
    
    # Test sample times
    test_times = [
        "Meeting at 18:50:00",
        "⏰ 10:30:00 Daily standup",
        "Release scheduled for 15:00 tomorrow"
    ]
    
    print("\nTesting sample times:")
    for i, text in enumerate(test_times, 1):
        print(f"\nTest {i}:\nOriginal: {text}")
        processed = process_message_text(text)
        print(f"Processed: {processed}")
        if text != processed:
            print("✅ Timezone conversion applied successfully")
        else:
            print("❌ No changes made")

def test_config():
    """Test that configuration is valid"""
    print("\n=== Testing configuration ===")
    
    # Check for bot token
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if token:
        masked_token = token[:5] + "..." + token[-5:]
        print(f"✅ Bot token found: {masked_token}")
    else:
        print("❌ Bot token not found. Set the TELEGRAM_BOT_TOKEN environment variable.")
    
    # Check for channels file
    if os.path.exists("monitored_channels.json"):
        with open("monitored_channels.json", "r") as f:
            channels = json.load(f)
        print(f"✅ Channels file found with {len(channels)} channels")
    else:
        print("❌ monitored_channels.json file not found")
    
    # Check for filters file
    if os.path.exists("user_filters.json"):
        with open("user_filters.json", "r") as f:
            filters = json.load(f)
        print(f"✅ Filters file found with {len(filters)} user-defined filters")
    else:
        print("❌ user_filters.json file not found")

def main():
    """Run all tests"""
    print("=== Telegram Channel Message Editor Bot Test ===")
    
    test_config()
    test_filters()
    test_timezone_conversion()
    
    print("\n=== Test Complete ===")
    print("""
If all tests passed, your bot should work correctly when connected to Telegram.
If there were any issues, check the README.md file for troubleshooting help.

To start the actual bot:
  python main.py
""")

if __name__ == "__main__":
    main()