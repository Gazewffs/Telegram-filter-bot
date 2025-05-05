import json
import re
import os
import logging
from config import STATIC_FILTERS

# Configure logging
logger = logging.getLogger(__name__)

# File to store user-defined filters
FILTERS_FILE = "user_filters.json"

def load_filters():
    """Load user-defined filters from the JSON file."""
    if not os.path.exists(FILTERS_FILE):
        # Create empty list
        save_filters([])
        return []
    
    try:
        with open(FILTERS_FILE, 'r') as f:
            filters = json.load(f)
            return filters
    except Exception as e:
        logger.error(f"Error loading filters: {e}")
        return []

def save_filters(filters_list):
    """Save filters to the JSON file.
    
    Args:
        filters_list: List of (pattern, replacement) tuples
    """
    try:
        with open(FILTERS_FILE, 'w') as f:
            json.dump(filters_list, f, indent=2)
        return True
    except Exception as e:
        logger.error(f"Error saving filters: {e}")
        return False

def add_filter(pattern, replacement):
    """Add a new filter pattern and replacement."""
    filters = load_filters()
    
    # Check if filter already exists with same pattern
    for i, (p, _) in enumerate(filters):
        if p == pattern:
            # Update replacement for existing pattern
            filters[i] = (pattern, replacement)
            return save_filters(filters)
    
    # Add new filter
    filters.append((pattern, replacement))
    return save_filters(filters)

def remove_filter(pattern):
    """Remove a filter by its pattern."""
    filters = load_filters()
    initial_count = len(filters)
    
    filters = [f for f in filters if f[0] != pattern]
    
    if len(filters) < initial_count:
        return save_filters(filters)
    
    return False

def list_filters():
    """Return a formatted list of all filters."""
    # Static filters from config
    static_filters = STATIC_FILTERS
    logger.info(f"Static filters from config: {static_filters}")
    
    # User-defined filters from JSON
    user_filters = load_filters()
    logger.info(f"Dynamic filters from user_filters.json: {user_filters}")
    
    # Combine both lists for display
    all_filters = static_filters + user_filters
    logger.info(f"Total filters: {len(all_filters)}")
    
    if not all_filters:
        return "No text filters configured."
    
    result = "📋 *Text Filters:*\n\n"
    result += "*Static filters (from config):*\n"
    
    for i, (pattern, replacement) in enumerate(static_filters, 1):
        result += f"{i}. `{pattern}` → `{replacement}`\n"
    
    if user_filters:
        result += "\n*User-defined filters:*\n"
        for i, (pattern, replacement) in enumerate(user_filters, 1):
            result += f"{i}. `{pattern}` → `{replacement}`\n"
    
    return result

def test_filter(text, pattern):
    """Test a regex pattern on a sample text."""
    try:
        # Compile the pattern
        regex = re.compile(pattern)
        
        # Find all matches
        matches = regex.findall(text)
        
        # Create result message
        result = f"*Pattern:* `{pattern}`\n\n*Text:* {text}\n\n"
        
        if matches:
            result += f"*Matches found:* {len(matches)}\n"
            for i, match in enumerate(matches, 1):
                if isinstance(match, tuple):
                    # If match is a tuple (for capture groups), show each group
                    match_str = ', '.join(match)
                    result += f"{i}. `{match_str}`\n"
                else:
                    result += f"{i}. `{match}`\n"
            
            # Show the text with the pattern applied/replaced
            try:
                replaced_text = regex.sub(r'*\1*', text)
                result += f"\n*With matches highlighted:*\n{replaced_text}"
            except:
                # In case of complex patterns where replacement fails
                pass
        else:
            result += "*No matches found*"
        
        return result
    except re.error as e:
        return f"*Error in regex pattern:* {e}"
    except Exception as e:
        return f"*Error testing filter:* {e}"

def get_all_filters():
    """Get all filters (dynamic and static)."""
    static_filters = STATIC_FILTERS
    user_filters = load_filters()
    return static_filters + user_filters