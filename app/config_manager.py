"""
Configuration Manager
Handles loading and saving bot configuration
"""
import json
import os
from typing import Dict, Any
from colorama import Fore

CONFIG_DIR = "config"
CONFIG_FILE = os.path.join(CONFIG_DIR, "bot_config.json")

DEFAULT_CONFIG = {
    "bot_name": "",
    "bot_channel_id": "",
    "permissions": {
        "say_command": "all",  # all, sponsor, mod, off
        "auto_reply": "all",   # all, sponsor, mod, off
        "welcome_users": "all", # all, off
        "jokes": "all",         # all, sponsor, mod, off
        "funny_sounds": "all"   # all, sponsor, mod, off
    },
    "moderation": {
        "emoji_limit": 5,
        "word_limit": 3,
        "timeout_normal": 300,  # seconds
        "timeout_mod": 60       # seconds
    },
    "cooldowns": {
        "say_delay": 10  # seconds between !say commands per user
    }
}

def ensure_config_dir():
    """Ensure config directory exists"""
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)

def load_config() -> Dict[str, Any]:
    """Load configuration from file or create default"""
    ensure_config_dir()
    
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                config = json.load(f)
                # Merge with defaults to ensure all keys exist
                return {**DEFAULT_CONFIG, **config}
        except Exception as e:
            print(Fore.YELLOW + f"Error loading config: {e}. Using defaults." + Fore.RESET)
            return DEFAULT_CONFIG.copy()
    else:
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG.copy()

def save_config(config: Dict[str, Any]):
    """Save configuration to file"""
    ensure_config_dir()
    
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4)
    except Exception as e:
        print(Fore.RED + f"Error saving config: {e}" + Fore.RESET)

def get_config_value(config: Dict[str, Any], key_path: str, default=None):
    """Get nested config value using dot notation"""
    keys = key_path.split('.')
    value = config
    for key in keys:
        if isinstance(value, dict):
            value = value.get(key, default)
        else:
            return default
    return value

def validate_and_update_config(config: Dict[str, Any]) -> Dict[str, Any]:
    """Validate configuration and prompt for missing values"""
    updated = False
    
    # Bot name
    if not config.get("bot_name"):
        bot_name = input(Fore.CYAN + "Enter your bot name: " + Fore.RESET).strip()
        if bot_name:
            config["bot_name"] = bot_name
            updated = True
    
    # Bot channel ID
    if not config.get("bot_channel_id"):
        channel_id = input(Fore.CYAN + "Enter your bot's YouTube channel ID: " + Fore.RESET).strip()
        if channel_id:
            # Remove URL part if full URL was provided
            if "youtube.com/channel/" in channel_id:
                channel_id = channel_id.split("youtube.com/channel/")[-1]
            config["bot_channel_id"] = channel_id
            updated = True
    
    if updated:
        save_config(config)
        print(Fore.GREEN + "Configuration saved successfully!" + Fore.RESET)
    
    return config
