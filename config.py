import os

# Bot token from environment variable
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

# Timezone configuration
SOURCE_TIMEZONE = "Etc/GMT-14"     # Source timezone of timestamps in messages
TARGET_TIMEZONE = "Asia/Kolkata"   # Target timezone to convert timestamps to

# Message processing options
PROCESS_TEXT = True        # Process text messages
PROCESS_CAPTIONS = True    # Process captions in media messages
REPLY_ON_EDIT_FAILURE = True  # Reply with corrected text when editing fails

# Static filter rules to always apply (regex pattern, replacement)
# These will be applied in addition to user-defined filters
STATIC_FILTERS = [
    # Example: Convert 'urgent' (case insensitive) to 'URGENT'
    (r'(?i)\b(urgent)\b', 'URGENT'),
    # Example: Convert 'important' (case insensitive) to 'IMPORTANT'
    (r'(?i)\b(important)\b', 'IMPORTANT'),
    # Example: Replace a username with another
    (r'@Gazew_07', '@BILLIONAIREBOSS101'),
    # Example: Replace an emoji
    (r'🚧', '🚀')
]

# Optional user-specific configurations
# For advanced users or administrators
ADMIN_USER_IDS = []