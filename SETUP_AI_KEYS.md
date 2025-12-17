# 🔑 Hướng Dẫn Lấy API Keys Cho Multi-AI Bot

## 📌 TÓM TẮT NHANH

Bạn cần lấy API keys từ 3 providers (TẤT CẢ MIỄN PHÍ):

1. **Google Gemini** - 60 requests/phút ✅ BẮT BUỘC
2. **Cohere** - 100 requests/phút ✅ KHUYÊN DÙNG  
3. **Hugging Face** - Unlimited ⭐ TÙY CHỌN

---

## 🎯 BƯỚC 1: Google Gemini (BẮT BUỘC)

### 1.1 Truy cập trang tạo API key:
```
https://aistudio.google.com/app/apikey
```

### 1.2 Đăng nhập Google

### 1.3 Click nút **"Create API Key"**

### 1.4 Chọn project hiện có hoặc tạo mới:
- Nếu chưa có project → Click **"Create API key in new project"**
- Nếu đã có project → Chọn project đó

### 1.5 Copy API Key
- API key sẽ có dạng: `AIzaSy...` (khoảng 39 ký tự)
- Click icon copy hoặc select + Ctrl+C

### 1.6 Paste vào config:
Mở file: `config/bot_config.json`

Tìm dòng:
```json
"gemini_api_key": "YOUR_GEMINI_API_KEY_HERE",
```

Thay bằng:
```json
"gemini_api_key": "AIzaSy...PASTE_KEY_CỦA_BẠN",
```

---

## 🎯 BƯỚC 2: Cohere (KHUYÊN DÙNG)

### 2.1 Đăng ký tài khoản:
```
https://dashboard.cohere.com/welcome/register
```

### 2.2 Đăng nhập

### 2.3 Vào trang API Keys:
```
https://dashboard.cohere.com/api-keys
```

### 2.4 Click **"Create Trial Key"**
- Name: `YouTube Bot`
- Click **"Create"**

### 2.5 Copy API Key
- Key có dạng: `xxx...` (khoảng 40 ký tự)

### 2.6 Paste vào config:
```json
"cohere_api_key": "PASTE_COHERE_KEY_VÀO_ĐÂY",
```

---

## 🎯 BƯỚC 3: Hugging Face (TÙY CHỌN)

### 3.1 Đăng ký tài khoản:
```
https://huggingface.co/join
```

### 3.2 Vào trang Access Tokens:
```
https://huggingface.co/settings/tokens
```

### 3.3 Click **"New token"**
- Name: `YouTube Bot`
- Role: **Read** (đủ rồi)
- Click **"Generate a token"**

### 3.4 Copy token

### 3.5 Paste vào config:
```json
"huggingface_api_key": "hf_...PASTE_TOKEN",
```

**LƯU Ý:** HuggingFace có thể để trống `""` vẫn chạy được (dùng public API, chậm hơn)

---

## ✅ KIỂM TRA CONFIG HOÀN CHỈNH

Mở file: `config/bot_config.json`

Nó phải trông như thế này:

```json
{
  "bot_name": "ACNChatBot",
  "bot_channel_id": "UCb5yqCY0dkE30AH-jy6z5Jg",
  
  "ai": {
    "enabled": true,
    "gemini_api_key": "AIzaSyABCD1234...",
    "cohere_api_key": "xyz123abc...",
    "huggingface_api_key": "hf_ABC..."
  },
  
  "permissions": {
    ...
  }
}
```

---

## 🚀 CÀI ĐẶT THƯ VIỆN

Sau khi có API keys, cài các thư viện:

```powershell
python -m pip install google-generativeai cohere huggingface-hub
```

---

## 🎮 CHẠY BOT

```powershell
python main.py
```

Nếu thành công, bạn sẽ thấy:

```
🤖 Đang khởi tạo AI providers...
  ✓ Gemini Pro ready
  ✓ Cohere ready
  ✓ HuggingFace ready (với API token)

✓ Multi-AI Handler sẵn sàng với 3 providers:

  1. Google Gemini Pro (60/min)
  2. Cohere Command (100/min)
  3. HuggingFace Mistral (Unlimited)
```

---

## 🔧 TROUBLESHOOTING

### ❌ "Invalid API key" (Gemini)
- Kiểm tra bạn copy đúng key
- Đảm bảo không có khoảng trắng đầu/cuối
- Thử tạo key mới

### ❌ "cohere.core.api_error.UnauthorizedError"
- Đảm bảo bạn đã active tài khoản Cohere qua email
- Thử tạo Trial Key mới

### ❌ HuggingFace chậm
- Tạo access token để tăng tốc
- Hoặc để trống vẫn chạy được (chậm hơn)

### ❌ Tất cả providers đều lỗi
- Kiểm tra kết nối internet
- Đảm bảo format JSON đúng (không thiếu dấu phẩy, ngoặc)
- Xem log chi tiết trong terminal

---

## 💡 TIPS

### Chỉ cần 1 provider:
Bot vẫn chạy nếu bạn chỉ có 1 API key (ví dụ: chỉ Gemini)

### Để trống keys không dùng:
```json
"cohere_api_key": "YOUR_COHERE_API_KEY_HERE",  // Bot sẽ bỏ qua
"huggingface_api_key": "",                      // Hoặc để trống
```

### Ưu tiên sử dụng:
1. Gemini (nhanh, chất lượng cao)
2. Cohere (khi Gemini hết quota)
3. HuggingFace (backup cuối cùng)

---

## 📊 CAPACITY

Với 3 providers:
- **Gemini:** 60 req/phút
- **Cohere:** 100 req/phút
- **HuggingFace:** Unlimited

**TỔNG:** Đủ cho 1000-3000 viewers đồng thời! ✅

---

## ⚠️ BẢO MẬT

**QUAN TRỌNG:** 
- KHÔNG share API keys với ai
- KHÔNG commit keys lên GitHub
- Giữ file `bot_config.json` bí mật

---

Có thắc mắc? Hỏi tôi! 🚀
