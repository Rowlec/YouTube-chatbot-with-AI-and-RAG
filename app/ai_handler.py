"""
Gemini Multi-Key Handler
Rotate giữa nhiều API keys để tăng rate limit
"""
import logging
from colorama import Fore
import random
import time
from typing import List, Optional

try:
    import google.generativeai as genai
    HAS_GEMINI = True
except ImportError:
    HAS_GEMINI = False
    print(Fore.YELLOW + "⚠ Gemini chưa cài: pip install google-generativeai" + Fore.RESET)

try:
    from .rag_handler import RAGKnowledgeBase
    HAS_RAG = True
except ImportError:
    HAS_RAG = False
    print(Fore.YELLOW + "⚠ RAG handler not available" + Fore.RESET)


class GeminiMultiKeyHandler:
    def __init__(self, api_keys):
        """
        Khởi tạo với nhiều API keys
        
        Args:
            api_keys: List các Gemini API keys hoặc dict config
        """
        # Xử lý input - có thể là list, dict, hoặc single string
        if isinstance(api_keys, str):
            api_keys = [api_keys]
        elif isinstance(api_keys, dict):
            # Backward compatibility với config cũ
            old_key = api_keys.get('gemini_api_key', '')
            new_keys = api_keys.get('gemini_api_keys', [])
            
            if new_keys and isinstance(new_keys, list):
                api_keys = new_keys
            elif old_key:
                api_keys = [old_key]
            else:
                api_keys = []
        
        # Filter valid keys
        self.api_keys = [key.strip() for key in api_keys 
                        if key and isinstance(key, str) and key.strip() and key != "YOUR_GEMINI_API_KEY_HERE"]
        
        if not self.api_keys:
            raise ValueError("❌ Không có API key hợp lệ!")
        
        self.current_key_index = 0
        self.key_usage = {key: {'count': 0, 'errors': 0, 'last_reset': time.time()} 
                         for key in self.api_keys}
        
        # Initialize RAG Knowledge Base
        self.rag = None
        if HAS_RAG:
            try:
                self.rag = RAGKnowledgeBase('config/knowledge.json')
                print(Fore.GREEN + f"  ✓ RAG Knowledge Base: {len(self.rag.knowledge)} entries loaded" + Fore.RESET)
            except Exception as e:
                print(Fore.YELLOW + f"  ⚠ RAG failed to load: {e}" + Fore.RESET)
                self.rag = None
        
        # System prompt - Tính cách của bot
        self.system_prompt = """Bạn là bot cho livestream của youtuber ACN. 
Quy tắc QUAN TRỌNG:
- Trả lời CỰC NGẮN 1-2 câu bằng tiếng Việt (max 150 ký tự)
- Dùng emoji phù hợp
- Phong cách GenZ, lầy lội, hài hước sigma skibidi
- Từ chối trả lời chính trị trừ khi có lợi cho Việt Nam

TUYỆT ĐỐI:
- Nếu có CONTEXT bên dưới, PHẢI trả lời dựa 100% vào CONTEXT đó
- KHÔNG được tự sáng tác thông tin nếu đã có CONTEXT"""
        
        # Khởi tạo models cho từng key
        self.models = {}
        self.chats = {}
        
        print(Fore.CYAN + "\n🤖 Đang khởi tạo Gemini Multi-Key Handler..." + Fore.RESET)
        
        failed_keys = []
        for i, key in enumerate(self.api_keys):
            try:
                genai.configure(api_key=key)
                model = genai.GenerativeModel('gemini-2.5-flash')
                self.models[key] = model
                self.chats[key] = model.start_chat(history=[])
                print(Fore.GREEN + f"  ✓ Gemini Key #{i+1} ready" + Fore.RESET)
            except Exception as e:
                print(Fore.YELLOW + f"  ⚠ Key #{i+1} failed: {e}" + Fore.RESET)
                failed_keys.append(key)
        
        # Remove failed keys
        for key in failed_keys:
            self.api_keys.remove(key)
        
        if not self.models:
            raise Exception("❌ Không có key nào hoạt động!")
        
        print(Fore.GREEN + f"\n✓ Gemini Multi-Key Handler: {len(self.api_keys)} keys active\n" + Fore.RESET)
    
    def _get_next_key(self) -> Optional[str]:
        """
        Lấy key tiếp theo theo round-robin
        Tự động bỏ qua keys có quá nhiều lỗi
        """
        attempts = 0
        while attempts < len(self.api_keys):
            # Round-robin
            key = self.api_keys[self.current_key_index]
            self.current_key_index = (self.current_key_index + 1) % len(self.api_keys)
            
            # Reset counter mỗi ngày (86400 giây)
            if time.time() - self.key_usage[key]['last_reset'] > 86400:
                self.key_usage[key]['count'] = 0
                self.key_usage[key]['errors'] = 0
                self.key_usage[key]['last_reset'] = time.time()
            
            # Skip keys có quá nhiều lỗi
            if self.key_usage[key]['errors'] < 5:
                return key
            
            attempts += 1
        
        # Nếu tất cả keys đều lỗi, reset và thử lại
        for key in self.api_keys:
            self.key_usage[key]['errors'] = 0
        
        return self.api_keys[0] if self.api_keys else None
    
    def get_response(self, user_message: str, user_name: str = "") -> str:
        """
        Lấy response từ Gemini với auto key rotation
        
        Args:
            user_message: Tin nhắn từ user
            user_name: Tên user
            
        Returns:
            Câu trả lời từ AI
        """
        # Thử tối đa 3 keys khác nhau
        for attempt in range(min(3, len(self.api_keys))):
            key = self._get_next_key()
            
            if not key:
                logging.error("[Gemini] Tất cả keys đều fail!")
                break
            
            try:
                # Configure key hiện tại
                genai.configure(api_key=key)
                
                # Get RAG context if available
                context = None
                if self.rag:
                    context = self.rag.get_context(user_message, max_length=300)
                    if context:
                        logging.info(f"[RAG] ✓ Context found for: '{user_message[:50]}...'")
                        print(Fore.GREEN + f"[RAG] ✓ Found context for: '{user_message[:60]}...'" + Fore.RESET)
                    else:
                        logging.info(f"[RAG] ✗ No context for: '{user_message[:50]}...'")
                        print(Fore.YELLOW + f"[RAG] ✗ No match for: '{user_message[:60]}...'" + Fore.RESET)
                
                # Tạo prompt với hoặc không có context
                if context:
                    prompt = f"""{self.system_prompt}

⚠️ CONTEXT - THÔNG TIN CHÍNH THỨC VỀ ACN (BẮT BUỘC PHẢI SỬ DỤNG):
{context}

User {user_name}: {user_message}

Bot (BẮT BUỘC trả lời dựa 100% vào CONTEXT trên, không được tự sáng tác):"""
                else:
                    prompt = f"{self.system_prompt}\n\nUser {user_name}: {user_message}\n\nBot:"
                
                # Gửi request qua chat để maintain context
                chat = self.chats[key]
                response = chat.send_message(prompt)
                
                # Lấy text
                if hasattr(response, 'text') and response.text:
                    ai_response = response.text.strip()
                else:
                    logging.warning(f"[Gemini] No text in response")
                    continue
                
                # Thêm mention tên user vào đầu response (nếu có user_name)
                if user_name:
                    ai_response = f"@{user_name} {ai_response}"
                
                # Giới hạn độ dài
                if len(ai_response) > 200:
                    ai_response = ai_response[:197] + "..."
                
                # Update usage
                self.key_usage[key]['count'] += 1
                
                key_num = self.api_keys.index(key) + 1
                logging.info(f"[Gemini Key #{key_num}] '{user_message}' -> '{ai_response}'")
                
                return ai_response
                
            except Exception as e:
                # Đánh dấu key bị lỗi
                self.key_usage[key]['errors'] += 1
                
                key_num = self.api_keys.index(key) + 1
                error_msg = str(e)
                logging.warning(f"[Gemini Key #{key_num}] Error: {error_msg}")
                
                # Nếu lỗi rate limit, thử key khác ngay
                if "429" in error_msg or "quota" in error_msg.lower() or "resource" in error_msg.lower():
                    logging.info(f"[Gemini Key #{key_num}] Rate limited, switching key...")
                    continue
                
                # Nếu lỗi khác, thử lại với key khác
                continue
        
        # Tất cả keys đều fail
        fallbacks = [
            "Úi zời oi bot đang bị limit rồi, anh em chờ tí nha! 🙏",
            "Ôi không, bot bị quá tải rồi! Anh em đợi tí nha! ⏳",
            "Huhu, bot mệt quá không trả lời được! Anh em thông cảm nha! 😢",
        ]
        return random.choice(fallbacks)
    
    def get_stats(self) -> str:
        """Lấy thống kê sử dụng keys"""
        stats = []
        for i, key in enumerate(self.api_keys):
            usage = self.key_usage[key]
            stats.append(f"Key #{i+1}: {usage['count']} requests, {usage['errors']} errors")
        return "\n".join(stats)
    
    def reset_conversation(self):
        """Reset tất cả conversations"""
        for key in self.api_keys:
            if key in self.models:
                self.chats[key] = self.models[key].start_chat(history=[])
        logging.info("All conversations reset")
    
    def is_available(self) -> bool:
        """Kiểm tra có key nào available không"""
        return len(self.models) > 0
