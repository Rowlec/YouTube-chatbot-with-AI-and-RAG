# 🔑 Cách thêm nhiều Gemini API Keys

## 📝 Hướng dẫn

### Bước 1: Lấy API Keys

**Cách 1: Dùng 1 tài khoản Google (Tối đa ~10 keys)**

1. Vào: https://aistudio.google.com/app/apikey
2. Đăng nhập tài khoản Google
3. Click **"Create API Key"** nhiều lần
4. Copy từng key

**Cách 2: Tạo nhiều tài khoản Gmail (Unlimited keys!)**

1. Tạo Gmail mới: acnbot1@gmail.com, acnbot2@gmail.com...
2. Mỗi Gmail vào: https://aistudio.google.com/app/apikey
3. Tạo 1-2 keys mỗi tài khoản
4. Copy tất cả keys

**Mẹo Gmail Alias:**
- Dùng: `youremail+bot1@gmail.com`, `youremail+bot2@gmail.com`
- Tất cả email đều về 1 inbox gốc!

---

### Bước 2: Thêm vào Config

Mở file: `config/bot_config.json`

```json
{
  "bot_name": "ACNChatBot",
  "bot_channel_id": "UCb5yqCY0dkE30AH-jy6z5Jg",
  
  "ai": {
    "enabled": true,
    "gemini_api_keys": [
      "AIzaSyCEb70gZDmeCbuh7i1QGbnkfE0Fw6VzX4M",
      "AIzaSyD_YOUR_KEY_2_HERE",
      "AIzaSyD_YOUR_KEY_3_HERE",
      "AIzaSyD_YOUR_KEY_4_HERE",
      "AIzaSyD_YOUR_KEY_5_HERE",
      "AIzaSyD_YOUR_KEY_6_HERE",
      "AIzaSyD_YOUR_KEY_7_HERE",
      "AIzaSyD_YOUR_KEY_8_HERE",
      "AIzaSyD_YOUR_KEY_9_HERE",
      "AIzaSyD_YOUR_KEY_10_HERE"
    ]
  }
}
```

**Lưu ý:**
- Xóa các dòng `YOUR_GEMINI_API_KEY_X` nếu không dùng
- Hoặc thay bằng key thật
- Có thể có 1 key hoặc 100 keys đều được!

---

### Bước 3: Test Bot

```powershell
python main.py
```

Bot sẽ hiển thị:
```
🤖 Đang khởi tạo Gemini Multi-Key Handler...
  ✓ Gemini Key #1 ready
  ✓ Gemini Key #2 ready
  ✓ Gemini Key #3 ready
  ...
  
✓ Gemini Multi-Key Handler: 10 keys active
```

---

## 📊 Capacity Calculation

| Số Keys | Requests/Ngày | Đủ cho Viewers |
|---------|--------------|----------------|
| 1 key   | 1,500        | ~200           |
| 5 keys  | 7,500        | ~1,000         |
| 10 keys | 15,000       | ~2,000 ✅       |
| 20 keys | 30,000       | ~4,000 ✅✅      |

**Với cooldown 3 giây:**
- 1000 viewers → Cần ~5-7 keys
- 2000 viewers → Cần ~10-15 keys  
- 3000 viewers → Cần ~15-20 keys

---

## ⚙️ Cách hoạt động

1. **Round-Robin Rotation:** Bot tự động xoay vòng giữa các keys
2. **Auto Skip Failed Keys:** Key nào lỗi quá 5 lần → tự động bỏ qua
3. **Daily Reset:** Counter reset mỗi 24h
4. **Smart Fallback:** Khi 1 key hết quota → chuyển ngay sang key khác

---

## 🎯 Khuyến nghị cho 1000-3000 viewers

```json
{
  "ai": {
    "enabled": true,
    "gemini_api_keys": [
      "KEY_1", "KEY_2", "KEY_3", "KEY_4", "KEY_5",
      "KEY_6", "KEY_7", "KEY_8", "KEY_9", "KEY_10",
      "KEY_11", "KEY_12", "KEY_13", "KEY_14", "KEY_15"
    ]
  },
  "cooldowns": {
    "ai_ask": 3
  }
}
```

**→ 15 keys + cooldown 3s = Đủ cho 3000+ viewers!**

---

## 🔍 Monitor Usage

Trong bot log, bạn sẽ thấy:
```
[Gemini Key #1] 'câu hỏi' -> 'câu trả lời'
[Gemini Key #2] 'câu hỏi' -> 'câu trả lời'
[Gemini Key #3] Rate limited, switching key...
[Gemini Key #4] 'câu hỏi' -> 'câu trả lời'
```

→ Bot tự động chuyển key khi cần!

---

## ✅ Hoàn tất!

Bot đã sẵn sàng! Chỉ cần:
1. Thêm keys vào `config/bot_config.json`
2. Run `python main.py`
3. Enjoy! 🎉
