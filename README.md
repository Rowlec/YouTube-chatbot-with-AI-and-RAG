# YouTube Live Chat Bot

A feature-rich YouTube Live Chat Bot inspired by MeowBot, built with Python. This bot can interact with your YouTube live stream chat, respond to commands, moderate spam, and more!

## Features

### 🤖 Chat Commands
- **!say <message>** - Text-to-speech command (configurable permissions)
- **!hello** - Greet users with a welcome message
- **!joke** - Tell a random joke
- **!bye** - Say goodbye with a farewell message
- **!so** - Give a shoutout to users
- **!weather <city>** - Get weather information for a location
- **!ask <query>** - Search Wikipedia
- **!asksum <query>** - Get Wikipedia summary
- **!askser <query>** - Search Wikipedia and get results
- **!time** - Display current time
- **!help** - Show available commands

### 🛡️ Moderation Features
- **Emoji Spam Detection** - Limits excessive emoji usage
- **Word Spam Detection** - Prevents repeated word spam
- **Message Spam Detection** - Blocks repeated messages
- **User Timeouts** - Automatically timeout spammers
- **Different timeout durations** for moderators vs regular users
- **Owner bypass** - Channel owners are never timed out

### 🔧 Configurable Permissions
Each feature can be restricted to:
- **all** - Everyone can use
- **sponsor** - Channel members only
- **mod** - Moderators and owners only
- **off** - Feature disabled

### 📊 Logging
- All bot actions are logged to `logs/bot.log`
- Chat messages are color-coded by user type:
  - 🔴 Red: Channel Owner
  - 🔵 Blue: Moderators
  - 🟢 Green: Channel Members
  - ⚪ White: Regular viewers

## Prerequisites

- **Python 3.8 or higher**
- **YouTube Channel** for the bot account
- **Google Cloud Project** with YouTube Data API v3 enabled
- **OAuth 2.0 credentials** (client_secret.json)

## Installation

### Step 1: Clone or Download
```bash
git clone <your-repo-url>
cd YT-CHATBOT
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Set Up Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable **YouTube Data API v3**:
   - Go to "APIs & Services" > "Library"
   - Search for "YouTube Data API v3"
   - Click "Enable"
4. Create OAuth 2.0 credentials:
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "OAuth client ID"
   - Choose "Desktop app" as application type
   - Download the JSON file
5. Rename the downloaded file to `client_secret.json`
6. Place it in the `config/` directory

### Step 4: Configure the Bot

Run the bot for the first time:
```bash
python main.py
```

You'll be prompted to enter:
- **Bot name** - Your bot's display name
- **Bot channel ID** - Your bot account's YouTube channel ID
  - Find it at: `https://www.youtube.com/channel/YOUR_CHANNEL_ID`

## Usage

### Starting the Bot

1. Make sure you have a **live stream running** on YouTube
2. Run the bot:
   ```bash
   python main.py
   ```
3. Enter your **live stream URL** when prompted
4. The bot will authenticate (opens browser on first run)
5. Once connected, the bot will start listening to chat!

### First Run Authentication

On the first run, the bot will:
1. Open your default web browser
2. Ask you to sign in with your **bot account**
3. Request permissions to manage YouTube
4. Save credentials for future use (in `config/token.pickle`)

### Stopping the Bot

Press `Ctrl+C` to gracefully stop the bot. It will send an offline message before disconnecting.

## Configuration

Edit `config/bot_config.json` to customize settings:

```json
{
    "bot_name": "MyBot",
    "bot_channel_id": "YOUR_CHANNEL_ID",
    "permissions": {
        "say_command": "all",
        "auto_reply": "all",
        "welcome_users": "all",
        "jokes": "all",
        "funny_sounds": "all"
    },
    "moderation": {
        "emoji_limit": 5,
        "word_limit": 3,
        "timeout_normal": 300,
        "timeout_mod": 60
    },
    "cooldowns": {
        "say_delay": 10
    }
}
```

### Configuration Options

#### Permissions
- `say_command` - Who can use !say command
- `auto_reply` - Auto-reply feature (future)
- `welcome_users` - Who gets welcomed with !hello
- `jokes` - Who can request jokes
- `funny_sounds` - Sound effects (future)

Values: `"all"`, `"sponsor"`, `"mod"`, `"off"`

#### Moderation
- `emoji_limit` - Max emojis per message (default: 5)
- `word_limit` - Max same word repeats (default: 3)
- `timeout_normal` - Timeout duration for regular users in seconds (default: 300)
- `timeout_mod` - Timeout duration for moderators in seconds (default: 60)

#### Cooldowns
- `say_delay` - Cooldown between !say commands per user in seconds (default: 10)

## Project Structure

```
YT-CHATBOT/
├── main.py                 # Entry point
├── app/
│   ├── __init__.py
│   ├── bot_core.py         # Main bot logic
│   ├── auth_manager.py     # YouTube API authentication
│   ├── config_manager.py   # Configuration handling
│   ├── commands.py         # Command processing
│   └── moderation.py       # Spam detection & moderation
├── config/
│   ├── bot_config.json     # Bot configuration
│   ├── client_secret.json  # OAuth credentials (you provide)
│   └── token.pickle        # Saved auth tokens (auto-generated)
├── logs/
│   └── bot.log            # Bot activity logs
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Troubleshooting

### "client_secret.json not found"
- Make sure you downloaded OAuth credentials from Google Cloud Console
- Place the file in the `config/` directory
- Rename it to exactly `client_secret.json`

### "Could not find active live chat"
- Ensure your stream is **live** (not scheduled or ended)
- Wait a few seconds after starting the stream
- Verify the stream URL is correct

### "Authentication failed"
- Delete `config/token.pickle` and try again
- Make sure you're using the correct Google account (bot account)
- Check that YouTube Data API v3 is enabled in Google Cloud Console

### Bot not responding to commands
- Check if commands are typed correctly (must start with !)
- Verify permissions in `config/bot_config.json`
- Check `logs/bot.log` for errors

### Import errors
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Use Python 3.8 or higher

## Optional Features

### Weather Command
To use `!weather`, you need an API key from [OpenWeatherMap](https://openweathermap.org/api):
1. Sign up for a free account
2. Get your API key
3. Edit `app/commands.py` and replace `YOUR_OPENWEATHER_API_KEY`

### Text-to-Speech
The `!say` command currently sends text to chat. For actual TTS:
1. Install additional audio libraries
2. Implement audio playback in `app/commands.py`
3. Consider using `pyttsx3` or `gtts` with audio output

## Contributing

Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests
- Improve documentation

## Credits

Inspired by [MeowBot](https://github.com/ostuxcat/MeowBot) by ostuxcat

## License

MIT License - Feel free to use and modify!

## Disclaimer

- Use responsibly and follow YouTube's Terms of Service
- Don't spam or abuse the API
- Respect chat moderation guidelines
- Keep your OAuth credentials secure

## Support

If you encounter issues:
1. Check the troubleshooting section
2. Review `logs/bot.log` for errors
3. Ensure all prerequisites are met
4. Verify your Google Cloud project setup

---

**Happy Streaming! 🎮🤖**
