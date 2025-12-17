# YouTube Chatbot Setup Guide

Bot tương tác tự động cho YouTube Live Chat với AI (Ollama/Gemini), RAG knowledge base, và moderation system.

## 📋 Yêu cầu

- Python 3.8+
- YouTube Channel với Live Chat
- Ollama (cho local AI) hoặc Gemini API keys
- YouTube Data API credentials

## 🚀 Cài đặt

### 1. Clone Repository

```bash
git clone <repository-url>
cd YT-CHATBOT
```

### 2. Cài đặt Dependencies

```bash
pip install -r requirements.txt
```

### 3. Cấu hình YouTube API

#### Bước 1: Tạo Google Cloud Project
1. Truy cập [Google Cloud Console](https://console.cloud.google.com/)
2. Tạo project mới hoặc chọn project có sẵn
3. Enable **YouTube Data API v3**

#### Bước 2: Tạo OAuth 2.0 Credentials
1. Vào **APIs & Services** → **Credentials**
2. Click **Create Credentials** → **OAuth client ID**
3. Chọn **Desktop app**
4. Download file JSON credentials
5. Đổi tên thành `client_secret.json` và đặt vào thư mục `config/`

#### Bước 3: Lấy Channel ID
1. Vào kênh YouTube của bạn
2. Lấy Channel ID từ URL hoặc trong About section
3. Format: `UCxxxxxxxxxxxxxxxxxxxxxx`

### 4. Cấu hình Bot

Copy file template và chỉnh sửa:

```bash
cp config/bot_config.example.json config/bot_config.json
```

Chỉnh sửa `config/bot_config.json`:

```json
{
  "bot_channel_id": "YOUR_YOUTUBE_CHANNEL_ID",
  "ai": {
    "provider": "ollama",
    "ollama_model": "gemma2",
    "ollama_host": "http://localhost:11434",
    "gemini_api_keys": [
      "YOUR_GEMINI_API_KEY_1",
      "YOUR_GEMINI_API_KEY_2"
    ]
  }
}
```

### 5. Cấu hình AI Provider

#### Option A: Ollama (Local AI - Recommended)

1. Cài đặt Ollama: https://ollama.ai/
2. Pull model:
   ```bash
   ollama pull gemma2
   ```
3. Start Ollama service
4. Set provider trong `bot_config.json`:
   ```json
   "provider": "ollama"
   ```

#### Option B: Gemini API

1. Lấy API keys tại: https://makersuite.google.com/app/apikey
2. Thêm vào `gemini_api_keys` trong `bot_config.json`
3. Set provider:
   ```json
   "provider": "gemini"
   ```

### 6. Customize Knowledge Base

Chỉnh sửa `config/knowledge.json` để thêm thông tin về kênh, streamer, FAQ của bạn:

```json
{
  "your_topic": {
    "keywords": ["keyword1", "keyword2", "câu hỏi thường gặp"],
    "content": "Câu trả lời của bot về topic này"
  }
}
```

## 🎮 Chạy Bot

### Lần đầu tiên (Authentication)

```bash
python main.py
```

Bot sẽ mở browser để bạn đăng nhập Google và cấp quyền. Token sẽ được lưu vào `config/token.pickle`.

### Lần sau

```bash
python main.py
```

Bot sẽ tự động kết nối đến livestream đang live.

## 🛠️ Cấu hình nâng cao

### Commands và Permissions

Trong `bot_config.json`, cấu hình quyền cho từng command:

```json
"permissions": {
  "say_command": "mod",     // Chỉ moderator
  "hello_command": "all",   // Tất cả mọi người
  "ask_command": "all"      // Tất cả (có cooldown)
}
```

### Moderation Settings

```json
"moderation": {
  "emoji_spam_limit": 5,           // Số emoji tối đa
  "word_spam_limit": 8,            // Số từ lặp lại
  "message_spam_limit": 3,         // Số tin nhắn giống nhau
  "timeout_duration_regular": 600  // Timeout 10 phút
}
```

### Auto Messages

Bot tự động gửi tin nhắn định kỳ mỗi 5 phút trong `app/bot_core.py`:

```python
self.auto_messages = [
    "Message 1",
    "Message 2",
    "Message 3"
]
```

## 📚 Commands có sẵn

| Command | Description | Permission |
|---------|-------------|------------|
| `!hello` | Chào bot | all |
| `!bye` | Tạm biệt | all |
| `!ask <question>` | Hỏi AI với RAG | all (7s cooldown) |
| `!joke` | Kể joke | all |
| `!weather <city>` | Thời tiết | all |
| `!time <timezone>` | Giờ hiện tại | all |
| `!discord` | Link Discord | all |
| `!acn` | Thông tin ACN | all |
| `!say <message>` | Bot nói thay | mod |
| `!so <channel>` | Shoutout | mod |

## 🔧 Testing

Test các module riêng lẻ:

```bash
# Test Ollama connection
python test_ollama.py

# Test Gemini API
python test_gemini.py

# Test RAG knowledge base
python test_rag.py

# Quick test all
python test_quick.py
```

## 🔒 Bảo mật

**QUAN TRỌNG:** Không commit các file sau lên Git:

- `config/bot_config.json` (chứa API keys)
- `config/client_secret.json` (OAuth credentials)
- `config/token.pickle` (access token)

File `.gitignore` đã được cấu hình sẵn.

## 🐛 Troubleshooting

### Bot không kết nối được

- Kiểm tra có livestream đang live không
- Verify `bot_channel_id` đúng
- Xóa `token.pickle` và authenticate lại

### AI không trả lời

**Ollama:**
- Check Ollama service đang chạy: `ollama list`
- Verify model đã pull: `ollama pull gemma2`

**Gemini:**
- Check API keys còn quota
- Xem logs để biết key nào bị rate limit

### RAG không match đúng

- Kiểm tra keywords trong `knowledge.json`
- Thêm nhiều variations cho keywords
- Xem logs `[RAG]` để debug matching

## 📝 Logs

Logs được lưu tại `logs/bot.log` với rotating (max 5MB x 3 files).

## 🤝 Contributing

1. Fork repository
2. Tạo feature branch
3. Commit changes
4. Push và tạo Pull Request

## 📄 License

MIT License

---

**Made with ❤️ for YouTube Creators**
