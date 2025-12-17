"""
Command Handler
Processes chat commands like !say, !hello, !joke, etc.
"""
import time
import random
import logging
from datetime import datetime, timedelta
from colorama import Fore

try:
    import pyjokes
    HAS_JOKES = True
except ImportError:
    HAS_JOKES = False

try:
    import wikipedia
    HAS_WIKIPEDIA = True
except ImportError:
    HAS_WIKIPEDIA = False

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

try:
    from gtts import gTTS
    HAS_TTS = True
except ImportError:
    HAS_TTS = False

try:
    from .ai_handler import GeminiMultiKeyHandler
    HAS_GEMINI = True
except ImportError:
    HAS_GEMINI = False

try:
    from .ollama_handler import OllamaHandler
    HAS_OLLAMA = True
except ImportError:
    HAS_OLLAMA = False

class CommandHandler:
    def __init__(self, bot):
        self.bot = bot
        self.user_cooldowns = {}
        self.processing_commands = set()  # Track currently processing commands
        
        # Khởi tạo AI Handler (Gemini hoặc Ollama)
        self.ai_handler = None
        ai_config = self.bot.config.get('ai', {})
        ai_enabled = ai_config.get('enabled', False)
        provider = ai_config.get('provider', 'gemini')
        
        print(Fore.CYAN + f"[AI] Enabled: {ai_enabled}, Provider: {provider}" + Fore.RESET)
        
        if ai_enabled:
            try:
                if provider == 'ollama':
                    if not HAS_OLLAMA:
                        raise ImportError("Ollama handler not available. `pip install ollama`")
                    
                    ollama_model = ai_config.get('ollama_model', 'llama3')
                    ollama_host = ai_config.get('ollama_host', 'http://localhost:11434')
                    self.ai_handler = OllamaHandler(model=ollama_model, host=ollama_host)
                    print(Fore.GREEN + f"✓ AI Handler: Ollama (Model: {ollama_model})" + Fore.RESET)

                else: # Mặc định là Gemini
                    if not HAS_GEMINI:
                        raise ImportError("Gemini handler not available")
                    
                    self.ai_handler = GeminiMultiKeyHandler(ai_config)
                    print(Fore.GREEN + f"✓ AI Handler: Gemini Multi-Key" + Fore.RESET)
                    
            except Exception as e:
                print(Fore.YELLOW + f"⚠ AI disabled: {e}" + Fore.RESET)
                import traceback
                traceback.print_exc()
                self.ai_handler = None
        else:
            print(Fore.YELLOW + "[AI] Disabled in config" + Fore.RESET)
        
    def check_permission(self, author, permission_type: str) -> bool:
        """Check if user has permission for a command"""
        permission = self.bot.config['permissions'].get(permission_type, 'all')
        
        if permission == 'off':
            return False
        elif permission == 'all':
            return True
        elif permission == 'mod':
            return author.isChatModerator or author.isChatOwner
        elif permission == 'sponsor':
            return author.isChatSponsor or author.isChatModerator or author.isChatOwner
        
        return False
    
    def check_cooldown(self, author, command: str) -> bool:
        """Check if user is on cooldown for a command"""
        cooldown_seconds = self.bot.config['cooldowns'].get('say_delay', 10)
        
        if cooldown_seconds == 0:
            return True
        
        key = f"{author.channelId}_{command}"
        now = datetime.now()
        
        if key in self.user_cooldowns:
            last_used = self.user_cooldowns[key]
            if now - last_used < timedelta(seconds=cooldown_seconds):
                remaining = cooldown_seconds - (now - last_used).seconds
                self.bot.send_message(
                    f"{author.name} Vui lòng đợi {remaining} giây trước khi dùng lệnh này lại."
                )
                return False
        
        self.user_cooldowns[key] = now
        return True
    
    def process_command(self, chat_item):
        """Process a command from chat"""
        message = chat_item.message.lower()
        author = chat_item.author
        
        # Extract command and arguments
        parts = message.split(' ', 1)
        command = parts[0]
        args = parts[1] if len(parts) > 1 else ''
        
        # Command routing
        if command in ['!say', '-say']:
            self.cmd_say(author, args)
        elif command in ['!hello', '-hello']:
            self.cmd_hello(author)
        elif command == '!joke':
            self.cmd_joke(author)
        elif command == '!bye':
            self.cmd_bye(author)
        elif command == '!so':
            self.cmd_shoutout(author)
        elif command == '!weather':
            self.cmd_weather(author, args)
        elif command in ['!ask', '!asksum', '!askser']:
            self.cmd_wikipedia(author, command, args)
        elif command == '!time':
            self.cmd_time(author)
        elif command == '!discord':
            self.cmd_discord(author)
        elif command == '!acn':
            self.cmd_acn(author)
        elif command == '!help':
            self.cmd_help(author)
    
    def cmd_say(self, author, text: str):
        """Text-to-speech command"""
        if not self.check_permission(author, 'say_command'):
            self.bot.send_message(f"{author.name} Bạn không có quyền sử dụng lệnh này.")
            return
        
        if not self.check_cooldown(author, 'say'):
            return
        
        if not text:
            self.bot.send_message(f"{author.name} Vui lòng nhập nội dung. Cách dùng: !say <tin nhắn>")
            return
        
        # Send acknowledgment
        self.bot.send_message(f"🔊 {author.name} nói: {text}")
        logging.info(f"Say command from {author.name}: {text}")
        
        # Optional: TTS implementation
        # This would require additional audio playback setup
    
    def cmd_hello(self, author):
        """Welcome command"""
        if not self.check_permission(author, 'welcome_users'):
            return
        
        greetings = [
            "Chào mừng đến với stream! 👋",
            "Xin chào! Hy vọng bạn đang vui vẻ! 😊",
            "Chào bạn! Rất vui được gặp bạn! 🎉",
            "Chào mừng! Hôm nay của bạn thế nào? ☀️",
            "Xin chào! Cảm ơn bạn đã tham gia! 💙"
        ]
        
        greeting = random.choice(greetings)
        self.bot.send_message(f"{author.name} {greeting}")
    
    def cmd_joke(self, author):
        """Tell a joke"""
        if not self.check_permission(author, 'jokes'):
            self.bot.send_message(f"{author.name} Bạn không có quyền sử dụng lệnh này.")
            return
        
        if not HAS_JOKES:
            self.bot.send_message(f"{author.name} Tính năng truyện cười chưa khả dụng.")
            return
        
        try:
            # Vietnamese jokes
            vietnamese_jokes = [
                "Tại sao lập trình viên thích đi ra ngoài vào ban đêm? Vì ban ngày có quá nhiều bug! 🐛",
                "Có 10 loại người trên thế giới: Người hiểu hệ nhị phân và người không hiểu! 😄",
                "Tại sao Java developer đeo kính? Vì họ không thấy C# được! 👓",
                "Làm sao để giết một lập trình viên? Thay đổi requirement liên tục! 😅",
                "Bug đâu phải là lỗi, đó là tính năng chưa được ghi chép! 📝"
            ]
            joke = random.choice(vietnamese_jokes)
            self.bot.send_message(f"{author.name} {joke}")
        except Exception as e:
            logging.error(f"Joke error: {e}")
            self.bot.send_message(f"{author.name} Úi, bot đang ngại ngùng quá! 😅")
    
    def cmd_bye(self, author):
        """Goodbye command"""
        farewells = [
            "Tạm biệt! Chúc bạn một ngày tốt lành! 👋",
            "Hẹn gặp lại! Giữ gìn sức khỏe nhé! 💙",
            "Bye bye! Cảm ơn bạn đã xem! 🌟",
            "Gặp lại sau nhé! Luôn tuyệt vời nha! ✨",
            "Tạm biệt! Quay lại sớm nhé! 🎊"
        ]
        
        farewell = random.choice(farewells)
        self.bot.send_message(f"{author.name} {farewell}")
    
    def cmd_shoutout(self, author):
        """Give a shoutout"""
        if author.isChatSponsor or author.isChatOwner or author.isChatModerator:
            self.bot.send_message(f"🎉 Shoutout cho {author.name}! Cảm ơn bạn đã ủng hộ! 💙")
        else:
            self.bot.send_message(f"{author.name} Shoutout cho bạn! 👋")
    
    def cmd_weather(self, author, location: str):
        """Get weather for a location"""
        if not HAS_REQUESTS:
            self.bot.send_message(f"{author.name} Weather feature not available.")
            return
        
        if not location:
            self.bot.send_message(f"{author.name} Please provide a location. Usage: !weather <city>")
            return
        
        try:
            # Using a free weather API (you'll need an API key for production)
            # This is a placeholder implementation
            API_KEY = "YOUR_OPENWEATHER_API_KEY"  # Get from openweathermap.org
            url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={API_KEY}&units=metric"
            
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                temp = data['main']['temp']
                description = data['weather'][0]['description']
                self.bot.send_message(
                    f"{author.name} Weather in {location}: {temp}°C with {description}"
                )
            else:
                self.bot.send_message(f"{author.name} Couldn't find weather for '{location}'")
        except Exception as e:
            logging.error(f"Weather error: {e}")
            self.bot.send_message(f"{author.name} Weather service temporarily unavailable.")
    
    def cmd_wikipedia(self, author, command: str, query: str):
        """Search Wikipedia or use AI"""
        if not query:
            self.bot.send_message(f"{author.name} Vui lòng nhập câu hỏi. Cách dùng: !ask <câu hỏi>")
            return
        
        # Prevent duplicate processing of same query
        cmd_key = f"{author.channelId}_ask_{query}"
        if cmd_key in self.processing_commands:
            logging.warning(f"[AI] Already processing: {cmd_key}")
            return
        
        self.processing_commands.add(cmd_key)
        
        try:
            # Ưu tiên dùng AI nếu có
            print(Fore.CYAN + f"[DEBUG] AI handler status: {self.ai_handler is not None}" + Fore.RESET)
            
            if self.ai_handler:
                print(Fore.CYAN + f"[DEBUG] Using AI handler for query: '{query}'" + Fore.RESET)
                # Check cooldown
                if not self.check_cooldown(author, 'ai_ask'):
                    self.processing_commands.discard(cmd_key)
                    return
                
                try:
                    logging.info(f"[AI Request] {author.name}: '{query}'")
                    # Lấy response từ AI (synchronous - chờ đến khi có response)
                    ai_response = self.ai_handler.get_response(query, author.name)
                    
                    # Validate AI response
                    if not ai_response or not ai_response.strip():
                        logging.warning(f"[AI] Returned empty response, using fallback")
                        ai_response = "Xin lỗi, tôi đang suy nghĩ quá nhiều! 🤔"
                    
                    logging.info(f"[AI Response] '{ai_response}'")
                    print(Fore.GREEN + f"[AI] Response: '{ai_response[:80]}...'" + Fore.RESET)
                    
                    # Không mention username - YouTube tự động mention khi reply
                    self.bot.send_message(ai_response)
                    self.processing_commands.discard(cmd_key)
                    return
                    
                except Exception as e:
                    logging.error(f"[AI Error] {e}")
                    print(Fore.RED + f"[AI Error] {e}" + Fore.RESET)
                    # Send fallback message instead of using Wikipedia
                    self.bot.send_message("Hmm, để tôi nghĩ lại nhé... 💭")
                    self.processing_commands.discard(cmd_key)
                    return
            else:
                print(Fore.YELLOW + "[DEBUG] AI handler not available, using Wikipedia fallback" + Fore.RESET)
            
            # Fallback: Wikipedia (nếu AI không có hoặc lỗi)
            if not HAS_WIKIPEDIA:
                self.bot.send_message(f"{author.name} Tính năng tìm kiếm chưa khả dụng.")
                self.processing_commands.discard(cmd_key)
                return
            
            # Thử tiếng Việt trước
            wikipedia.set_lang('vi')
            
            if command == '!asksum':
                summary = wikipedia.summary(query, sentences=2)
                self.bot.send_message(f"{author.name} {summary}")
            elif command == '!askser':
                results = wikipedia.search(query, results=3)
                results_text = ", ".join(results)
                self.bot.send_message(f"{author.name} Có thể bạn tìm: {results_text}")
            else:
                # Default: tìm summary
                summary = wikipedia.summary(query, sentences=2)
                # Giới hạn độ dài
                if len(summary) > 200:
                    summary = summary[:197] + "..."
                self.bot.send_message(f"{author.name} {summary}")
                
        except wikipedia.exceptions.DisambiguationError as e:
            options = ", ".join(e.options[:3])
            self.bot.send_message(f"{author.name} Có nhiều kết quả. Thử: {options}")
        except wikipedia.exceptions.PageError:
            # Thử lại với tiếng Anh
            try:
                wikipedia.set_lang('en')
                summary = wikipedia.summary(query, sentences=2)
                if len(summary) > 200:
                    summary = summary[:197] + "..."
                self.bot.send_message(f"{author.name} {summary}")
            except:
                self.bot.send_message(f"{author.name} Không tìm thấy thông tin về '{query}'")
        except Exception as e:
            logging.error(f"Wikipedia error: {e}")
            self.bot.send_message(f"{author.name} Có lỗi xảy ra khi tìm kiếm.")
        finally:
            # Always remove from processing set
            self.processing_commands.discard(cmd_key)
    
    def cmd_time(self, author):
        """Get current time"""
        current_time = datetime.now().strftime("%H:%M:%S")
        current_date = datetime.now().strftime("%d/%m/%Y")
        self.bot.send_message(f"{author.name} Bây giờ là: {current_time} ngày {current_date}")
    
    def cmd_discord(self, author):
        """Share Discord server link"""
        if not self.check_permission(author, 'discord_command'):
            return
        
        # Lấy link Discord từ config hoặc dùng link mặc định
        discord_link = self.bot.config.get('links', {}).get('discord', 'https://discord.gg/YOUR_SERVER')
        
        messages = [
            f"🎮 {author.name} Discord server: {discord_link} - Vào chơi cùng ae nhé!",
            f"💬 {author.name} Join Discord của mình tại: {discord_link}",
            f"🌟 {author.name} Tham gia cộng đồng Discord: {discord_link}"
        ]
        
        self.bot.send_message(random.choice(messages))
    
    def cmd_acn(self, author):
        """Show information about ACN channel"""
        if not self.check_permission(author, 'acn_command'):
            return
        
        # Lấy thông tin ACN từ config
        acn_info = self.bot.config.get('acn_info', {
            'description': 'Kênh của ACN - Content sáng tạo và giải trí!',
            'youtube': 'youtube.com/@ACN',
        })
        
        messages = [
            f"📺 {author.name} {acn_info.get('description', 'Kênh ACN')} Đăng ký & bật chuông nhé! 🔔",
            f"🎬 {author.name} Cảm ơn bạn đã ủng hộ ACN! {acn_info.get('subscribe_count', '')} subscribers và đang tăng! 🚀",
            f"⭐ {author.name} Theo dõi ACN để không bỏ lỡ video mới! {acn_info.get('youtube', '')} 📺"
        ]
        
        self.bot.send_message(random.choice(messages))
    
    def cmd_help(self, author):
        """Show help message"""
        help_text = (
            "Lệnh: !say <text>, !hello, !joke, !bye, !so, "
            "!weather <city>, !ask <câu hỏi>, !time, !discord, !acn, !help"
        )
        
        # Thông báo nếu AI đang hoạt động
        if self.ai_handler:
            help_text += " | 🤖 AI đang bật!"
        
        self.bot.send_message(f"{author.name} {help_text}")
