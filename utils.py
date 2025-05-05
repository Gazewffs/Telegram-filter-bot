import re
import logging
import pytz
from datetime import datetime
from filter_manager import get_all_filters
from config import SOURCE_TIMEZONE, TARGET_TIMEZONE

# Configure logging
logger = logging.getLogger(__name__)

def apply_text_filters(text):
    """Apply text filters to the message text"""
    filters = get_all_filters()
    logger.info(f"Got {len(filters)} filters to apply")
    logger.info(f"Original text: {text}")
    
    modified_text = text
    
    # Apply each filter pattern
    for pattern, replacement in filters:
        logger.info(f"Applying filter: pattern='{pattern}', replacement='{replacement}'")
        
        try:
            text_before = modified_text
            modified_text = re.sub(pattern, replacement, modified_text)
            
            if modified_text != text_before:
                logger.info(f"Text changed: '{text_before}' -> '{modified_text}'")
        except Exception as e:
            logger.error(f"Error applying filter pattern '{pattern}': {e}")
    
    logger.info(f"Final modified text: {modified_text}")
    return modified_text

def convert_timezone(text):
    """
    Find timestamps in the text and convert them from SOURCE_TIMEZONE to TARGET_TIMEZONE
    """
    logger.info(f"Attempting to convert timestamps in: {text}")
    logger.info(f"Source timezone: {SOURCE_TIMEZONE}, Target timezone: {TARGET_TIMEZONE}")
    
    # Define source and target timezone objects
    source_tz = pytz.timezone(SOURCE_TIMEZONE)
    target_tz = pytz.timezone(TARGET_TIMEZONE)
    
    # Various timestamp patterns to match
    # Main pattern: HH:MM:SS DD/MM/YYYY or DD/MM/YYYY HH:MM:SS
    timestamp_pattern = r'(\d{1,2}:\d{2}(?::\d{2})?\s+\d{1,2}/\d{1,2}/\d{4}|\d{1,2}/\d{1,2}/\d{4}\s+\d{1,2}:\d{2}(?::\d{2})?)'
    
    # Additional patterns
    # Just time pattern: HH:MM:SS or HH:MM
    time_pattern_1 = r'(\d{1,2}:\d{2}(?::\d{2})?)'
    
    # Time with emoji pattern: ⏰ HH:MM:SS or ⏰ HH:MM
    time_pattern_2 = r'⏰\s*(\d{1,2}:\d{2}(?::\d{2})?)'
    
    modified_text = text
    
    # Function to convert a timestamp to the target timezone
    def convert_timestamp(match):
        timestamp_str = match.group(1)
        try:
            # Parse the timestamp based on its format
            if '/' in timestamp_str:
                # Has date component
                if timestamp_str.index(':') < timestamp_str.index('/'):
                    # Format: HH:MM:SS DD/MM/YYYY
                    time_part, date_part = timestamp_str.split()
                    dt_format = '%H:%M:%S %d/%m/%Y' if ':' in time_part else '%H:%M %d/%m/%Y'
                else:
                    # Format: DD/MM/YYYY HH:MM:SS
                    date_part, time_part = timestamp_str.split()
                    dt_format = '%d/%m/%Y %H:%M:%S' if ':' in time_part else '%d/%m/%Y %H:%M'
                
                dt = datetime.strptime(timestamp_str, dt_format)
            else:
                # Time only: HH:MM:SS or HH:MM
                time_only = timestamp_str
                today = datetime.now()
                dt_format = '%H:%M:%S' if time_only.count(':') == 2 else '%H:%M'
                
                try:
                    dt = datetime.strptime(f"{today.day}/{today.month}/{today.year} {time_only}", f"%d/%m/%Y {dt_format}")
                except ValueError:
                    # If it's just a time reference without context, just convert the time
                    hours, minutes = map(int, time_only.split(':')[:2])
                    seconds = 0
                    if time_only.count(':') == 2:
                        seconds = int(time_only.split(':')[2])
                    
                    src_time = datetime.now(source_tz).replace(hour=hours, minute=minutes, second=seconds)
                    tgt_time = src_time.astimezone(target_tz)
                    
                    # Format time as HH:MM:SS or HH:MM based on input
                    if time_only.count(':') == 2:
                        return f"{tgt_time.hour:02d}:{tgt_time.minute:02d}:{tgt_time.second:02d}"
                    else:
                        return f"{tgt_time.hour:02d}:{tgt_time.minute:02d}"
            
            # Create datetime with source timezone
            dt_with_tz = source_tz.localize(dt)
            
            # Convert to target timezone
            dt_target = dt_with_tz.astimezone(target_tz)
            
            # Format the converted timestamp to match the original format
            converted_timestamp = dt_target.strftime(dt_format)
            
            logger.info(f"Converted timestamp: '{timestamp_str}' -> '{converted_timestamp}'")
            return converted_timestamp
        
        except Exception as e:
            logger.error(f"Error converting timestamp '{timestamp_str}': {e}")
            return timestamp_str  # If conversion fails, keep the original
    
    # Find and convert timestamps using the main pattern
    timestamp_matches = re.findall(timestamp_pattern, modified_text)
    logger.info(f"Found {len(timestamp_matches)} timestamp pattern matches using main pattern")
    
    for timestamp_str in timestamp_matches:
        try:
            converted = convert_timestamp(re.match(r'(' + re.escape(timestamp_str) + r')', timestamp_str))
            modified_text = modified_text.replace(timestamp_str, converted)
        except Exception as e:
            logger.error(f"Error replacing timestamp '{timestamp_str}': {e}")
    
    # Find and convert time-only patterns
    time_matches_1 = re.findall(time_pattern_1, modified_text)
    logger.info(f"Found {len(time_matches_1)} timestamp matches using additional pattern 1")
    
    for time_str in time_matches_1:
        try:
            converted = convert_timestamp(re.match(r'(' + re.escape(time_str) + r')', time_str))
            modified_text = modified_text.replace(time_str, converted)
        except Exception as e:
            logger.error(f"Error replacing time '{time_str}': {e}")
    
    # Find and convert emoji time patterns
    emoji_time_matches = re.findall(time_pattern_2, modified_text)
    logger.info(f"Found {len(emoji_time_matches)} timestamp matches using additional pattern 2")
    
    for time_str in emoji_time_matches:
        try:
            converted = convert_timestamp(re.match(r'(' + re.escape(time_str) + r')', time_str))
            modified_text = modified_text.replace(time_str, converted)
        except Exception as e:
            logger.error(f"Error replacing emoji time '{time_str}': {e}")
    
    logger.info(f"Total timestamps found: {len(timestamp_matches) + len(time_matches_1) + len(emoji_time_matches)}")
    
    return modified_text

def process_message_text(text):
    """
    Process a message text by applying text filters and timezone conversion
    """
    # First apply text replacements
    filtered_text = apply_text_filters(text)
    
    # Then convert timestamps
    result = convert_timezone(filtered_text)
    
    return result