#!/usr/bin/env python3
import os
import logging
from bot import main

if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO,
        filename='bot.log'
    )
    
    logger = logging.getLogger(__name__)
    logger.info("Starting Telegram Channel Message Editor Bot")
    
    # Start the bot
    main()