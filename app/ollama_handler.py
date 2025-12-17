"""
Ollama AI Handler
Connects to a local Ollama instance to get AI responses.
"""
import ollama
import logging
from colorama import Fore

try:
    from .rag_handler import RAGKnowledgeBase
    HAS_RAG = True
except ImportError:
    HAS_RAG = False

class OllamaHandler:
    def __init__(self, model: str, host: str):
        """
        Initialize Ollama handler.
        
        Args:
            model: The name of the Ollama model to use (e.g., 'llama3').
            host: The URL of the Ollama host (e.g., 'http://localhost:11434').
        """
        self.model = model
        self.host = host
        self.client = ollama.Client(host=host)
        
        # Initialize RAG Knowledge Base
        self.rag = None
        if HAS_RAG:
            try:
                self.rag = RAGKnowledgeBase('config/knowledge.json')
                print(Fore.GREEN + f"  ✓ RAG Knowledge Base: {len(self.rag.knowledge)} entries loaded" + Fore.RESET)
            except Exception as e:
                print(Fore.YELLOW + f"  ⚠ RAG failed to load: {e}" + Fore.RESET)
                self.rag = None
        
        self.system_prompt = """Bạn là bot cho livestream của youtuber ACN. 
Quy tắc QUAN TRỌNG:
- Trả lời CỰC NGẮN 1-2 câu bằng TIẾNG VIỆT (max 150 ký tự)
- Dùng 1 hoặc 2 emoji phù hợp
- Phong cách GenZ, hài hước, sigma skibidi, không nói tục
- Từ chối trả lời chính trị trừ khi có lợi cho Việt Nam

QUY TẮC TUYỆT ĐỐI:
- Nếu có CONTEXT bên dưới, BẮT BUỘC phải trả lời dựa 100% vào CONTEXT đó
- KHÔNG được tự sáng tác thông tin nếu đã có CONTEXT
- CONTEXT là sự thật tuyệt đối về ACN, không được thay đổi hoặc bổ sung thêm"""
        logging.info(f"✓ Ollama Handler ready (Model: {model}, Host: {host})")

    def get_response(self, user_message: str, user_name: str = "") -> str:
        """
        Get AI response from local Ollama instance.
        
        Args:
            user_message: The user's message.
            user_name: The user's display name.
            
        Returns:
            AI response string.
        """
        try:
            # Get RAG context if available
            context = None
            if self.rag:
                context = self.rag.get_context(user_message, max_length=300)
                if context:
                    logging.info(f"[Ollama/RAG] ✓ Found context for: '{user_message[:50]}...'")
                    print(Fore.GREEN + f"[Ollama/RAG] ✓ Found context" + Fore.RESET)
                else:
                    logging.info(f"[Ollama/RAG] ✗ No context for: '{user_message[:50]}...'")
                    print(Fore.YELLOW + f"[Ollama/RAG] ✗ No match" + Fore.RESET)
            
            # Build prompt (with or without context)
            if context:
                # Có context - trả lời dựa vào knowledge base
                messages = [
                    {
                        'role': 'system',
                        'content': self.system_prompt
                    },
                    {
                        'role': 'user',
                        'content': f"""Dựa vào CONTEXT sau:
---
{context}
---
Trả lời câu hỏi của user: "{user_message}"
"""
                    }
                ]
            else:
                # Không có context - trả lời bằng kiến thức chung
                logging.info(f"[Ollama] No RAG context, using general knowledge for: '{user_message}'")
                messages = [
                    {
                        'role': 'system',
                        'content': self.system_prompt
                    },
                    {
                        'role': 'user',
                        'content': f'Trả lời câu hỏi: "{user_message}"'
                    }
                ]

            logging.info(f"[Ollama] Sending request to model: {self.model}")
            response = self.client.chat(
                model=self.model,
                messages=messages
            )
            
            ai_response = response['message']['content'].strip()
            
            # Thêm mention tên user vào đầu response (nếu có user_name)
            if user_name:
                ai_response = f"@{user_name} {ai_response}"
            
            # Giới hạn độ dài để không bị YouTube API từ chối
            if len(ai_response) > 190:
                ai_response = ai_response[:187] + "..."

            logging.info(f"[Ollama] Response: '{ai_response}'")
            return ai_response

        except Exception as e:
            logging.error(f"[Ollama] Error: {e}")
            return "Lỗi rồi, không kết nối được với AI local (Ollama). Bạn chắc là đã bật Ollama lên chưa?"

    def is_available(self) -> bool:
        """Check if handler is available"""
        return True
