# YouTube Live Chat Bot 🤖

A feature-rich, intelligent YouTube Live Chat Bot with AI integration, RAG knowledge base, auto-moderation, and chat reliability optimization. Perfect for Vietnamese YouTube streamers.

**Key Updates:** Now uses pytchat with automatic Data API fallback for maximum reliability!

---

## ✨ Core Features

### 🤖 AI Chat Responses
- **Local AI (Ollama)** - Run AI locally on your machine, 100% free
- **Google Gemini API** - Cloud-based powerful AI with multi-key rotation
- **RAG Knowledge Base** - Answers based on custom knowledge (53+ entries)
- **Smart Context** - RAG matches keywords and provides relevant answers
- **Auto-reply** - Responds to `!ask` commands with AI context

### 💬 Chat Commands
| Command | Usage | Permission |
|---------|-------|-----------|
| `!ask <question>` | Ask AI with knowledge base | all |
| `!hello` | Bot greets user | all |
| `!bye` | Bot says goodbye | all |
| `!joke` | Random joke | all |
| `!weather <city>` | Weather info | all |
| `!time [timezone]` | Current time | all |
| `!discord` | Discord server link | all |
| `!acn` | Channel info | all |
| `!say <message>` | Bot sends message | mod |
| `!so <channel>` | Shoutout | mod |

### 🛡️ Auto Moderation
- **Emoji spam detection** - Limit emojis per message
- **Word spam detection** - Detect repeated words
- **Message spam detection** - Block duplicate messages
- **Auto timeout** - Automatically timeout spammers
- **Mod-aware** - Shorter timeout for moderators
- **Owner immunity** - Streamers are protected

### 📢 Auto Messages
- **Periodic messages** - Sends messages every 3 minutes
- **Customizable** - Edit messages in `bot_config.json`
- **Discord promotion** - Links to your Discord server
- **Command tutorial** - Teaches users about !ask command

### 🔗 Chat Reliability
- **Pytchat first** - Uses web-based chat (no quota)
- **Automatic fallback** - Falls back to YouTube Data API if needed
- **Periodic retry** - Switches back to pytchat when available
- **Quota optimization** - Minimizes API usage

---

## 📋 Prerequisites

Before starting, you need:

- **Python 3.8 or higher** ([Download](https://www.python.org/downloads/))
- **YouTube Channel** for the bot account
- **Google Cloud Project** with YouTube Data API v3 enabled
- **OAuth 2.0 Credentials** (client_secret.json)
- **AI Setup**: Either Ollama (local) OR Gemini API keys

---

## 🚀 Installation (Step by Step)

### Step 1: Install Python & Clone Project

```bash
# Verify Python installation
python --version

# Clone or download the project
git clone <your-repo-url>
cd YT-CHATBOT
```

### Step 2: Install Python Dependencies

```bash
# Install all required packages
pip install -r requirements.txt

# Verify installation
python -c "import pytchat; print('✓ pytchat installed')"
```

### Step 3: Set Up Google Cloud Project & OAuth

Follow these steps to get your OAuth credentials:

1. **Create a Google Cloud Project:**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Click "Select a Project" → "New Project"
   - Name it "YT Chat Bot" and create

2. **Enable YouTube Data API v3:**
   - In the console, go to "APIs & Services" → "Library"
   - Search for **"YouTube Data API v3"**
   - Click the result, then click "Enable"
   - Wait 30 seconds for activation

3. **Create OAuth Credentials:**
   - Go to "APIs & Services" → "Credentials"
   - Click "Create Credentials" → "OAuth client ID"
   - If prompted, first create an "OAuth consent screen":
     - User Type: "External"
     - Fill required fields (app name, user support email, developer email)
     - Scopes: Leave default
     - Test users: Add your email
     - Save and continue
   - Back to Credentials, click "Create Credentials" → "OAuth client ID"
   - Application type: **"Desktop app"**
   - Name: "YT Chat Bot"
   - Click "Create"

4. **Download & Place Credentials:**
   - Click the download icon (⬇️) on your created credential
   - A JSON file downloads as `client_secret_xxxxx.json`
   - Rename it to `client_secret.json`
   - Move it to the `config/` folder:
     ```bash
     move client_secret.json config/client_secret.json
     ```

**Verify:** You should see `config/client_secret.json` (not with a random suffix).

### Step 4: Set Up AI (Choose ONE)

#### Option A: Ollama (Recommended - Free, Local)

**Why Ollama?**
- ✅ 100% free - no API costs
- ✅ Privacy - data stays on your machine
- ✅ No rate limits - unlimited requests
- ✅ Offline capable - works without internet
- ✅ Multiple models - Gemma2, Llama3, Mistral, etc.

**Install Ollama:**

1. Download from [ollama.com](https://ollama.com)
2. Install and run (it starts automatically)
3. Pull a model:
   ```bash
   ollama pull gemma2
   ```
   (Or `ollama pull llama2` for a different model)

4. Verify it's running:
   ```bash
   ollama list
   ```

5. Configure bot (`config/bot_config.json`):
   ```json
   {
     "ai": {
       "enabled": true,
       "provider": "ollama",
       "ollama_model": "gemma2",
       "ollama_host": "http://localhost:11434"
     }
   }
   ```

**Done!** Ollama runs in the background automatically.

#### Option B: Gemini API (Cloud-based)

**Pros:**
- ✅ No installation needed
- ✅ Powerful model (Gemini 2.5 Flash)
- ⚠️ Limited free tier: 15 requests/minute per key

**Get Gemini API Keys:**

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key (starts with `AIzaSy...`)
5. Repeat 3-5 times to create multiple keys (avoid rate limits)

6. Configure bot (`config/bot_config.json`):
   ```json
   {
     "ai": {
       "enabled": true,
       "provider": "gemini",
       "gemini_api_keys": [
         "AIzaSy...KEY_1...",
         "AIzaSy...KEY_2...",
         "AIzaSy...KEY_3..."
       ]
     }
   }
   ```

Bot automatically rotates between keys when one hits the rate limit.

### Step 5: Configure Bot Settings

1. **Copy template config:**
   ```bash
   copy config\bot_config.example.json config\bot_config.json
   ```

2. **Edit `config/bot_config.json`:**

   ```json
   {
     "bot_name": "My Chat Bot",
     "bot_channel_id": "UCxxxxxxxxxxxxxx",
     
     "ai": {
       "enabled": true,
       "provider": "ollama",
       "ollama_model": "gemma2",
       "ollama_host": "http://localhost:11434"
     },
     
     "permissions": {
       "say_command": "mod",
       "hello_command": "all",
       "joke_command": "all",
       "ask_command": "all"
     },
     
     "moderation": {
       "emoji_spam_limit": 5,
       "word_spam_limit": 8,
       "message_spam_limit": 3,
       "timeout_duration_regular": 600,
       "timeout_duration_mod": 60
     },
     
     "messages": {
       "startup": "đang online! 🤖",
       "shutdown": "đã offline! 👋"
     }
   }
   ```

3. **Find your Channel ID:**
   - Go to your YouTube channel
   - URL: `youtube.com/@YourChannelName`
   - Go to "About" tab → Share channel → Copy link: `youtube.com/channel/UC...`
   - The `UC...` part is your Channel ID

### Step 6: Customize Knowledge Base

Edit `config/knowledge.json` to add facts about your channel:

```json
{
  "streamer_name": {
    "keywords": [
      "ai là gì",
      "ai là ai",
      "thông tin về streamer"
    ],
    "content": "XYZ is an amazing streamer with 500k+ subscribers!"
  },
  "channel_discord": {
    "keywords": [
      "discord",
      "link discord",
      "server dc"
    ],
    "content": "Join our Discord: discord.gg/mycommunity"
  }
}
```

The more keywords you add, the better the bot matches user questions!

---

## 🎮 Running the Bot

### First Time Setup

```bash
python main.py
```

The bot will:
1. **Authenticate** - Opens your browser (sign in with bot account)
2. **Request permissions** - Allows YouTube Data API access
3. **Save tokens** - Stores credentials in `config/token.pickle` for next runs
4. **Prompt for stream URL** - Enter your live stream URL

### Starting the Bot (After First Run)

```bash
python main.py
```

Then:
1. Enter your livestream URL when prompted
2. Bot authenticates instantly (uses saved token)
3. Bot connects and listens to chat
4. Responds to commands and sends periodic messages

### Stopping the Bot

Press `Ctrl+C` - Bot sends a goodbye message and exits gracefully.

---

## 🧪 Testing & Validation

### Test pytchat Without a Live Stream

The bot supports both pytchat (web-based) and YouTube Data API. Test pytchat reliability:

```bash
# Test on a past livestream video
python app/test_pytchat_standalone.py YpF_s0QqP6o

# Or on another video
python app/test_pytchat_standalone.py YOUR_VIDEO_ID
```

**Output Example:**
```
Testing pytchat on video: YpF_s0QqP6o
============================================================

[Test] pytchat.create on YpF_s0QqP6o
  ✓ create() initialized, is_alive=True
    [@User1] hello
    [@User2] test message
    [@User3] hey bot!
  ✓ create() SUCCESS: Read 5 messages

============================================================
[Summary]
  create():  ✓ WORKS

✓ Pytchat can read chat from this video!
```

This confirms pytchat works for your streams!

### Test RAG Knowledge Base

```bash
python test_rag.py
```

Verifies the knowledge base loads and keyword matching works.

### Test AI Responses

```bash
python test_ai.py
```

Tests AI with your configured model (Ollama or Gemini).

---

## ⚙️ Configuration Options

### Permission Levels

```json
"permissions": {
  "say_command": "mod"
}
```

Values:
- `"all"` - Everyone
- `"sponsor"` - Channel members only
- `"mod"` - Moderators and owner
- `"off"` - Feature disabled

### Auto Message Interval

Change how often the bot sends periodic messages:

```json
// In app/bot_core.py line 38
self.auto_message_interval = 180  // 3 minutes (in seconds)
```

### Pytchat with Cookies (Advanced)

If pytchat fails on restricted streams, provide browser cookies:

1. Export cookies from YouTube watch page using extension ("Get cookies.txt")
2. Save to `config/cookies.txt` (Netscape format)
3. In `config/bot_config.json`:
   ```json
   {
     "pytchat_cookies": "config/cookies.txt",
     "pytchat_retry_sec": 90
   }
   ```

---

## 🐛 Troubleshooting

### "client_secret.json not found"
```
Error: No such file in 'config/' directory
```
**Fix:**
- Download OAuth credentials from Google Cloud Console
- Rename to exactly `client_secret.json`
- Ensure it's in the `config/` folder, not root

### "Could not find active live chat"
```
Error: Live chat ID not found
```
**Fix:**
- Stream must be **actively LIVE** (not scheduled or ended)
- Wait 10-15 seconds after starting stream
- Verify stream URL is correct: `youtube.com/watch?v=VIDEOID`

### "Cannot connect to Ollama"
```
Error: Connection refused to http://localhost:11434
```
**Fix:**
```bash
# Verify Ollama is running
ollama list

# If not installed, download from ollama.com
# If installed, it runs automatically on startup
```

### "429 Rate limit exceeded" (Gemini API)
```
Error: Too many requests from this API key
```
**Fix:**
- Add more API keys to `gemini_api_keys` array (create 5-10 keys)
- Bot automatically rotates between keys
- Or use Ollama instead (unlimited)

### "Authentication failed"
```
Error: OAuth token invalid or expired
```
**Fix:**
```bash
# Delete saved token and re-authenticate
del config\token.pickle
python main.py
# Follow browser authentication flow again
```

### "Bot doesn't respond to commands"
**Fix:**
1. Command format must be: `!ask question here`
2. Check permissions in `bot_config.json` for that command
3. Check `logs/bot.log` for errors:
   ```bash
   type logs\bot.log
   ```

### "Import errors" (ModuleNotFoundError)
```bash
# Re-install dependencies
pip install -r requirements.txt --upgrade

# Or install specific package
pip install pytchat ollama google-generativeai
```

---

## 📊 Logging & Debugging

All bot activity is logged to `logs/bot.log`. Check it when troubleshooting:

```bash
# View last 20 lines
tail -20 logs\bot.log

# Or open in editor
code logs\bot.log
```

**Log includes:**
- Authentication status
- Chat connections (pytchat vs API)
- Command processing
- AI responses
- Moderation actions
- Errors and warnings

---

## 📁 Project Structure

```
YT-CHATBOT/
├── app/
│   ├── bot_core.py              # Main bot logic & chat listener
│   ├── ai_handler.py            # Gemini API handler with multi-key
│   ├── ollama_handler.py        # Local Ollama AI handler
│   ├── rag_handler.py           # Knowledge base search & matching
│   ├── commands.py              # Chat commands (!ask, !hello, etc.)
│   ├── moderation.py            # Spam detection & auto-timeout
│   ├── auth_manager.py          # YouTube OAuth authentication
│   ├── config_manager.py        # Config file loader
│   ├── test_pytchat_standalone.py  # Pytchat validation tool
│   └── __init__.py
│
├── config/
│   ├── bot_config.json          # Main config (edit this!)
│   ├── bot_config.example.json  # Template
│   ├── knowledge.json           # RAG knowledge base (53+ entries)
│   ├── client_secret.json       # OAuth credentials (you provide)
│   └── token.pickle             # Auto-saved authentication token
│
├── logs/
│   └── bot.log                  # Activity & error logs
│
├── main.py                      # Entry point - run this!
├── requirements.txt             # Python dependencies
├── README.md                    # This guide
├── SETUP.md                     # Detailed setup guide
└── .gitignore
```

---

## ✨ Features Comparison: Ollama vs Gemini

| Feature | Ollama | Gemini API |
|---------|--------|-----------|
| **Cost** | Free | Free tier (15 req/min) |
| **Setup** | Install app | Just API key |
| **Rate limit** | Unlimited | 15 requests/minute per key |
| **Privacy** | Local (your PC) | Cloud (Google) |
| **Internet needed** | No | Yes |
| **Model choice** | Gemma2, Llama3, Mistral | Gemini 2.5 Flash only |
| **Speed** | Depends on PC | Always fast |
| **Default** | ✅ Recommended | ❌ Use if PC weak |

---

## 🎯 Next Steps

1. ✅ **Install Python & dependencies** - `pip install -r requirements.txt`
2. ✅ **Set up OAuth credentials** - Download `client_secret.json`
3. ✅ **Choose AI** - Install Ollama OR get Gemini keys
4. ✅ **Edit config** - Customize `bot_config.json`
5. ✅ **Customize knowledge** - Edit `knowledge.json`
6. ✅ **Test** - Run `python app/test_pytchat_standalone.py VIDEO_ID`
7. ✅ **Go live** - Start your stream and run `python main.py`

---

## 🚀 Advanced Setup

### Switch AI Providers at Runtime

Just change `config/bot_config.json`:
```json
// Use Ollama
"provider": "ollama"

// Switch to Gemini
"provider": "gemini"
```

Restart bot - no code changes needed!

### Use Different Ollama Models

```bash
# See available models
ollama list

# Pull a new model
ollama pull llama2
ollama pull mistral
ollama pull neural-chat

# Update config to use it
# "ollama_model": "mistral"
```

### Manage Multiple Gemini Keys

Bot rotates automatically:
```json
"gemini_api_keys": [
  "KEY_1",
  "KEY_2",
  "KEY_3",
  "KEY_4"
]
```

When all keys hit the rate limit (15 req/min each), bot will queue requests and eventually succeed.

---

## 💬 Common Questions

**Q: Do I need to keep Ollama open?**
A: No, Ollama runs as a background service automatically after installation.

**Q: Can I use Ollama + Gemini together?**
A: No, pick one. But you can switch between them anytime by editing `config/bot_config.json`.

**Q: Why does my bot crash when stream ends?**
A: The bot stops when chat is no longer available. Run it again when you stream next.

**Q: How do I add more knowledge to the RAG base?**
A: Edit `config/knowledge.json` - add keywords and responses. More keywords = better matching!

**Q: Can I run multiple bots?**
A: Yes! Create separate folders with different `client_secret.json` and configs.

**Q: Does the bot work offline?**
A: Only if using Ollama (no internet needed). Gemini API requires internet.

---

## 📞 Support & Troubleshooting

1. **Check logs first:**
   ```bash
   type logs\bot.log
   ```

2. **Run tests:**
   ```bash
   python test_ai.py
   python test_rag.py
   python app/test_pytchat_standalone.py VIDEO_ID
   ```

3. **Verify setup:**
   - `config/client_secret.json` exists
   - Ollama running OR Gemini keys valid
   - `config/bot_config.json` has correct settings

4. **Reset everything:**
   ```bash
   del config\token.pickle
   del logs\bot.log
   python main.py
   ```

---

## 📝 License & Disclaimer

- **MIT License** - Free to use and modify
- **Respect YouTube ToS** - Follow YouTube's Terms of Service
- **Keep credentials safe** - Never share `client_secret.json` or API keys
- **No spam** - Don't abuse the API or chat
- **Legal use only** - Use for legitimate streaming purposes

---

## 🙏 Credits

- Built for Vietnamese YouTube community
- Pytchat for web-based chat access
- Ollama for free local AI
- RAG system for accurate knowledge-based responses

---

**Happy Streaming! 🎮✨**

Made with ❤️ for content creators
