# YouTube Live Chat Bot

A feature-rich YouTube Live Chat Bot with AI integration, RAG knowledge base, and advanced moderation. Built with Python for Vietnamese YouTube streamers.

## ✨ Tính năng chính

### 🤖 AI-Powered Chat
- **Local AI với Ollama** - Chạy AI hoàn toàn trên máy của bạn, miễn phí 100%
- **Gemini API** - Sử dụng Google Gemini với multi-key rotation
- **RAG Knowledge Base** - Bot trả lời chính xác dựa trên knowledge base tùy chỉnh
- **Auto-reply intelligent** - Trả lời tự động với context awareness
- **Mention user** - Bot tự động tag người hỏi khi trả lời

### 💬 Chat Commands
- **!ask <câu hỏi>** - Hỏi AI với RAG knowledge base
- **!hello** - Chào người dùng
- **!bye** - Tạm biệt
- **!joke** - Kể joke ngẫu nhiên
- **!weather <city>** - Thông tin thời tiết
- **!time [timezone]** - Hiển thị giờ hiện tại
- **!discord** - Link Discord server
- **!acn** - Thông tin về ACN
- **!so <channel>** - Shoutout channel (mod only)
- **!say <message>** - Bot nói thay (mod only)

### 🛡️ Auto Moderation
- **Emoji Spam Detection** - Giới hạn số emoji trong tin nhắn
- **Word Spam Detection** - Phát hiện từ lặp lại
- **Message Spam Detection** - Chặn tin nhắn spam giống nhau
- **Auto Timeout** - Tự động timeout người spam (10 phút)
- **Mod Protection** - Timeout ngắn hơn cho moderators
- **Owner Immunity** - Owner không bị timeout

### 📢 Auto Messages
- **Periodic Messages** - Tự động gửi tin nhắn mỗi 5 phút
- **Discord Promotion** - Quảng bá Discord server
- **Command Tutorial** - Hướng dẫn sử dụng !ask
- **Custom Messages** - Tùy chỉnh tin nhắn tự động

### 🔧 Configurable Permissions
Each feature can be restricted to:
- **all** - Everyone can use
- **sponsor** - Channel members only
- **mod** - Moderators and owners only
- **off** - Feature disabled

### 📊 Logging
- All bot actions are logged to `logs/bot.log`
- C📋 Yêu cầu hệ thống

- **Python 3.8+**
- **YouTube Channel** cho bot account
- **Google Cloud Project** với YouTube Data API v3 enabled
- **OAuth 2.0 credentials** (client_secret.json)
- **Ollama** (khuyến nghị - miễn phí) HOẶC **Gemini API keys**
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
Setup AI (Chọn 1 trong 2 options)

#### 🎯 Option A: Ollama (Khuyến nghị - 100% miễn phí, chạy local)

**Tại sao chọn Ollama?**
- ✅ **Hoàn toàn miễn phí** - Không giới hạn requests
- ✅ **Bảo mật** - Data không ra khỏi máy bạn
- ✅ **Không cần API key** - Setup đơn giản
- ✅ **Nhanh** - Response time thấp
- ✅ **Nhiều models** - Gemma2, Llama3, Mistral...

**Cài đặt Ollama:**
🚀 Sử dụng

### Khởi động Bot

1. **Start AI service (nếu dùng Ollama):**
   
   Ollama tự động chạy background, không cần làm gì. Nếu muốn verify:
   ```bash
   ollama list
   ```

2. **Bật YouTube Livestream** - Bot chỉ hoạt động khi stream đang live

3. **Run bot:**
   ```bash
   python main.py
   ```

4. **Lần đầu authenticate:**
   - Browser sẽ mở
   - Đăng nhập bằng **bot account** (không phải account chính của bạn)
   - Cấp quyền YouTube Data API
   - Token sẽ lưu vào `config/token.pickle`

5. **Bot sẽ tự động:**
   - Kết nối đến livestream
   ⚙️ Configuration

### Bot Config (`config/bot_config.json`)

```json
{
  "bot_name": "Your Bot Name",
  "bot_channel_id": "YOUR_YOUTUBE_CHANNEL_ID",
  
  "ai": {
    "enabled": true,
    "provider": "ollama",              // "ollama" hoặc "gemini"
    "ollama_model": "gemma2",          // Model cho Ollama
    "ollama_host": "http://localhost:11434",
    "gemini_api_keys": [               // Nhiều keys cho Gemini
      "KEY_1",
      "KEY_2"
    ]
  },
  
  "permissions": {
    "say_command": "mod",              // mod, all, off
    "hello_command": "all",
    "ask_command": "all"
  },
  
  "moderation": {
    "emoji_spam_limit": 5,             // Max emojis per message
    "word_spam_limit": 8,              // Max repeated words
    "message_spam_limit": 3,           // Max same messages
    "timeout_duration_regular": 600,   // 10 minutes timeout
    "timeout_duration_mod": 60         // 1 minute for mods
  },
  
  "cooldowns": {
    "say_command": 30,                 // seconds
    "joke_command": 10,
    "ai_ask": 7                        // AI response cooldown
 
   Edit `config/bot_config.json`:
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

**Ollama sẽ tự động chạy background service. Không cần start thủ công!**

#### 🌐 Option B: Gemini API (Cần API keys)

**Ưu điểm:**
- ✅ Không cần cài đặt local
- ✅ Model mạnh (Gemini 2.5 Flash)
- ⚠️ Giới hạn free tier: 15 requests/phút per key

**Setup Gemini API:**

1. **Lấy API keys:**
   - Truy cập: https://makersuite.google.com/app/apikey
   - Tạo API key (miễn phí)
   - Nên tạo nhiều keys (5-10 keys) để tránh rate limit

2. **Config bot:**
   
   Edit `config/bot_config.json`:
   ```json
   {
     "ai": {
       "enabled": true,
       "provider": "gemini",
       "gemini_api_keys": [
         "YOUR_GEMINI_API_KEY_1",
         "YOUR_GEMINI_API_KEY_2",
         "YOUR_GEMINI_API_KEY_3"
       ]
     }
   }
   ```

Bot sẽ tự động rotate giữa các keys khi bị rate limit.

### Step 5: Configure Bot Settings

Copy file template nếu chưa có:
```bash
copy config\bot_config.example.json config\bot_config.json
```

Edit các thông tin cần thiết trong `config/bot_config.json`:
- **bot_channel_id** - YouTube Channel ID của bot
- **links.discord** - Link Discord server của bạn
- **links.youtube** - Link kênh YouTube

### Step 6: Customize Knowledge Base

Edit `config/knowledge.json` để thêm thông tin về kênh/streamer của bạn:

```json
{
  "your_topic": {
    "keywords": ["keyword1", "từ khóa 2", "câu hỏi thường gặp"],
    "content": "Câu trả lời của bot về topic này"
  }
}
```

Bot sẽ tự động search keywords và trả lời dựa trên content.
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

Val## 🐛 Troubleshooting

### Ollama Issues

**"Connection refused" hoặc "Cannot connect to Ollama"**
```bash
# Verify Ollama đang chạy
ollama list
🔧 Advanced Setup

### So sánh Ollama vs Gemini

| Feature | Ollama (Local) | Gemini API |
|---------|----------------|------------|
| **Chi phí** | 100% miễn phí | Free tier có giới hạn |
| **Rate limit** | Không giới hạn | 15 req/min per key |
| **Bảo mật** | Data local | Data đi qua Google |
| **Setup** | Cần cài đặt | Chỉ cần API key |
| **Performance** | Phụ thuộc PC | Luôn nhanh (cloud) |
| **Offline** | Hoạt động offline | Cần internet |
| **Model** | Gemma2, Llama3... | Gemini 2.5 Flash |

**Khuyến nghị:**
- **Ollama (gemma2)** - Cho mọi trường hợp, đặc biệt streams dài
- **Gemini** - Nếu PC yếu hoặc muốn model mạnh hơn

### Switch Between Ollama & Gemini

Đơn giản chỉ cần đổi trong `config/bot_config.json`:

```json
// Dùng Ollama
"provider": "ollama"

// Dùng Gemini  
"provider": "gemini"
```

Restart bot là xong!

### Multiple Gemini Keys Rotation

Bot tự động rotate giữa nhiều keys để tránh rate limit:

```json
"gemini_api_keys": [
  "KEY_1",  // Key 1 bị limit -> switch sang Key 2
  "KEY_2",  // Key 2 bị limit -> switch sang Key 3
  "📂 Project Structure

```
YT-CHATBOT/
├── app/
│   ├── ai_handler.py           # Gemini multi-key handler
│   ├── ollama_handler.py       # Ollama local AI handler  
│   ├── rag_handler.py          # RAG knowledge base search
│   ├── commands.py             # Command processing
│   ├── bot_core.py             # Main bot logic
│   ├── moderation.py           # Spam detection & timeout
│   ├── auth_manager.py         # YouTube OAuth
│   └── config_manager.py       # Config loader
├── config/
│   ├── bot_config.json         # Main config (create from .example)
│   ├── bot_config.example.json # Template
│   ├── knowledge.json          # RAG knowledge base
│   ├── client_secret.json      # OAuth credentials (you provide)
│   └── token.pickle            # Saved tokens (auto-generated)
├── logs/
│   └── bot.log                 # Activity logs
├── main.py                     # Entry point
├── requirements.txt            # Dependencies
├── SETUP.md                    # Detailed setup guide
└── README.md                   # This file
```

## 🤝 Contributing

Contributions welcome! Feel free to:
- Report bugs via Issues
- Suggest features
- Submit Pull Requests
- Improve documentation
- Add more knowledge to `knowledge.json`

## 📚 Documentation

- **[SETUP.md](SETUP.md)** - Chi tiết setup từng bước
- **[MULTI_KEY_SETUP.md](MULTI_KEY_SETUP.md)** - Hướng dẫn setup multi Gemini keys
- **[SETUP_AI_KEYS.md](SETUP_AI_KEYS.md)** - Hướng dẫn lấy API keys

## 🎯 Roadmap

- [ ] Web dashboard để monitor bot
- [ ] Support thêm AI providers (OpenRouter, Claude)
- [ ] Voice commands với speech recognition
- [ ] Analytics và stats viewer engagement
- [ ] Multi-language support

## 📄 License

MIT License - Free to use and modify!

## ⚠️ Disclaimer

- Tuân thủ YouTube Terms of Service
- Không spam hoặc abuse API
- Giữ OAuth credentials an toàn
- Bot chỉ dùng cho mục đích hợp pháp

## 💬 Support

Nếu gặp vấn đề:
1. Xem [Troubleshooting](#-troubleshooting)
2. Check `logs/bot.log`
3. Test với `test_*.py` scripts
4. Verify setup theo [SETUP.md](SETUP.md)

## 🙏 Credits

- Developed for Vietnamese YouTube community
- Ollama integration for free local AI
- RAG system for accurate responses
- Special thanks to all contributors

---

**🎮 Happy Streaming! Made with ❤️ for YouTube Creators"
```
```

**Bot response chậm**
- Gemma2 (~2GB) nhanh nhất cho low-end PC
- Llama3 (~4GB) cần RAM nhiều hơn
- Thử model nhỏ hơn: `ollama pull phi3`

### Gemini API Issues

**"429 Rate limit exceeded"**
- Thêm nhiều API keys vào `gemini_api_keys` array
- Bot sẽ tự động rotate keys
- Free tier: 15 requests/phút per key

**"Invalid API key"**
- Check key có đúng format: `AIzaSy...`
- Tạo key mới tại: https://makersuite.google.com/app/apikey
- Verify key active (không expired)

### Bot Connection Issues

**"client_secret.json not found"**
- Download OAuth credentials từ Google Cloud Console
- Đặt vào `config/` folder
- Rename thành `client_secret.json`

**"Could not find active live chat"**
- Stream phải đang **LIVE** (không phải scheduled)
- Đợi 10-15 giây sau khi bật stream
- Check URL livestream đúng format

**"Authentication failed"**
- Delete `config/token.pickle`
- Run bot lại và authenticate
- Dùng đúng bot account (không phải account chính)

### RAG Not Working

**Bot không trả lời đúng dựa theo knowledge.json**
```bash
# Test RAG matching
python test_rag.py

# Kiểm tra keywords trong knowledge.json có đủ variations không
# Ví dụ: "cao bao nhiêu", "chiều cao", "bao nhiêu mét"
```

### General Issues

**Import errors**
```bash
pip install -r requirements.txt --upgrade
```

**Bot không respond commands**
- Check command format: `!ask câu hỏi`
- Verify permissions trong `bot_config.json`
- Xem logs: `logs/bot.log`  # Bot configuration
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
