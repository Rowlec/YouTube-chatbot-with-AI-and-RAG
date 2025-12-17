"""
Bot Core
Main bot logic and YouTube Live Chat integration
"""
import re
import time
import logging
from datetime import datetime
from typing import Optional
import pytchat
from colorama import Fore
from .config_manager import load_config, validate_and_update_config
from .auth_manager import get_authenticated_service
from .commands import CommandHandler
from .moderation import ModerationHandler

# Setup logging
logging.basicConfig(
    filename='logs/bot.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class YouTubeChatBot:
    def __init__(self):
        self.config = load_config()
        self.config = validate_and_update_config(self.config)
        self.youtube = None
        self.live_chat_id = None
        self.video_id = None
        self.bot_channel_id = self.config.get('bot_channel_id', '')  # Bot's own channel ID
        self.command_handler = CommandHandler(self)
        self.moderation_handler = ModerationHandler(self)
        self.user_cooldowns = {}  # Track user command cooldowns
        self.processed_message_ids = set()  # Track processed messages to avoid duplicates
        self.last_auto_message_time = time.time()  # Track last auto message
        self.auto_message_interval = 300  # 5 minutes in seconds
        
    def authenticate(self):
        """Authenticate with YouTube API"""
        print(Fore.CYAN + "\nAuthenticating with YouTube..." + Fore.RESET)
        try:
            self.youtube = get_authenticated_service()
            print(Fore.GREEN + "✓ Authentication successful!" + Fore.RESET)
            return True
        except Exception as e:
            print(Fore.RED + f"✗ Authentication failed: {e}" + Fore.RESET)
            logging.error(f"Authentication error: {e}")
            return False
    
    def get_live_stream_url(self) -> str:
        """Prompt user for live stream URL"""
        print()
        url = input(Fore.CYAN + "Enter your YouTube Live Stream URL: " + Fore.RESET).strip()
        return url
    
    def extract_video_id(self, url: str) -> Optional[str]:
        """Extract video ID from YouTube URL"""
        patterns = [
            r'youtube\.com/watch\?v=([a-zA-Z0-9_-]{11})',
            r'youtube\.com/live/([a-zA-Z0-9_-]{11})',
            r'youtu\.be/([a-zA-Z0-9_-]{11})'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None
    
    def get_live_chat_id(self, video_id: str) -> Optional[str]:
        """Get live chat ID for the video"""
        try:
            request = self.youtube.videos().list(
                part="liveStreamingDetails",
                id=video_id
            )
            response = request.execute()
            
            if response['items']:
                return response['items'][0]['liveStreamingDetails'].get('activeLiveChatId')
            return None
        except Exception as e:
            print(Fore.RED + f"Error getting live chat ID: {e}" + Fore.RESET)
            logging.error(f"Live chat ID error: {e}")
            return None
    
    def send_message(self, message: str):
        """Send a message to the live chat"""
        try:
            # Validate message
            if not message or not message.strip():
                logging.warning("Attempted to send empty message")
                print(Fore.YELLOW + f"⚠ Empty message blocked" + Fore.RESET)
                return
            
            # Ensure message is string and not too long
            message = str(message).strip()
            
            # Remove problematic characters that might cause API errors
            # YouTube API doesn't like some special chars in certain combinations
            import re
            message = re.sub(r'[\x00-\x08\x0B-\x0C\x0E-\x1F]', '', message)  # Remove control chars
            
            # Debug log
            print(Fore.CYAN + f"[DEBUG] Attempting to send: '{message[:100]}...' (len={len(message)})" + Fore.RESET)
            logging.info(f"Attempting to send message: '{message}'")
            
            if len(message) > 500:
                message = message[:497] + "..."
            
            self.youtube.liveChatMessages().insert(
                part="snippet",
                body={
                    "snippet": {
                        "liveChatId": self.live_chat_id,
                        "type": "textMessageEvent",
                        "textMessageDetails": {
                            "messageText": message
                        }
                    }
                }
            ).execute()
            logging.info(f"Bot message sent: {message}")
        except Exception as e:
            print(Fore.RED + f"Error sending message: {e}" + Fore.RESET)
            logging.error(f"Send message error: {e}")
    
    def timeout_user(self, channel_id: str, duration_seconds: int):
        """Timeout a user (temporary ban)"""
        try:
            # Don't timeout the bot itself or channel owner
            if channel_id == self.config.get('bot_channel_id'):
                return
            
            self.youtube.liveChatBans().insert(
                part="snippet",
                body={
                    "snippet": {
                        "liveChatId": self.live_chat_id,
                        "type": "temporary",
                        "banDurationSeconds": duration_seconds,
                        "bannedUserDetails": {
                            "channelId": channel_id
                        }
                    }
                }
            ).execute()
            logging.info(f"User {channel_id} timed out for {duration_seconds}s")
        except Exception as e:
            logging.error(f"Timeout error: {e}")
    
    def send_periodic_messages(self):
        """Send periodic promotional messages every 5 minutes"""
        current_time = time.time()
        
        if current_time - self.last_auto_message_time >= self.auto_message_interval:
            import random
            messages = [
                "Tham gia cộng đồng discord của ACN tại đây: discord.gg/acn 🎮💬",
                "Mọi người có thể sử dụng lệnh !ask <Câu hỏi> để trò chuyện với bot nhé <3 🤖✨",
                "Anh em nhớ làm theo lời khuyên của ACN: \"Hãy làm người thật tốt\" 🗿🗿💙"
            ]
            
            message = random.choice(messages)
            self.send_message(message)
            self.last_auto_message_time = current_time
            logging.info(f"Sent periodic message: {message}")
    
    def process_message(self, chat_item):
        """Process a chat message"""
        try:
            author = chat_item.author
            
            # Skip bot's own messages
            if author.channelId == self.bot_channel_id:
                return
            
            # Strip @ prefix from username if exists (YouTube API sometimes includes it)
            if hasattr(author, 'name') and author.name.startswith('@'):
                author.name = author.name[1:]
            
            # Skip duplicate messages (using content + author for better dedup)
            message_id = f"{author.channelId}_{chat_item.message}_{chat_item.timestamp}"
            if message_id in self.processed_message_ids:
                logging.debug(f"Skipping duplicate message: {message_id}")
                return
            self.processed_message_ids.add(message_id)
            
            # Clean old IDs (keep only last 100)
            if len(self.processed_message_ids) > 100:
                self.processed_message_ids = set(list(self.processed_message_ids)[-100:])
            
            message = chat_item.message.lower()
            
            # Color code by user type
            if author.isChatOwner:
                color = Fore.RED
            elif author.isChatModerator:
                color = Fore.BLUE
            elif author.isChatSponsor:
                color = Fore.GREEN
            else:
                color = Fore.WHITE
            
            print(f"{color}[{chat_item.datetime}] @{author.name}: {chat_item.message}{Fore.RESET}")
            logging.info(f"Processing message ID: {message_id} from {author.name}")
            
            # Check for moderation issues
            moderation_result = self.moderation_handler.check_message(chat_item)
            if not moderation_result['allowed']:
                return
            
            # Process commands
            if message.startswith('!'):
                self.command_handler.process_command(chat_item)
        
        except Exception as e:
            logging.error(f"Message processing error: {e}")
    
    def start_chat_listener(self):
        """Start listening to live chat"""
        print(Fore.GREEN + f"\n✓ Bot is now listening to chat!" + Fore.RESET)
        print(Fore.YELLOW + "Press Ctrl+C to stop\n" + Fore.RESET)
        
        # Send startup message
        bot_name = self.config.get('bot_name', 'Bot').upper()
        startup_msg = self.config.get('messages', {}).get('startup', 'ĐANG ONLINE! 🤖')
        self.send_message(f"{bot_name} {startup_msg}")
        
        # Create pytchat object
        chat = pytchat.create(video_id=self.video_id)
        
        try:
            while chat.is_alive():
                # Send periodic messages
                self.send_periodic_messages()
                
                for chat_item in chat.get().sync_items():
                    self.process_message(chat_item)
                time.sleep(0.1)
        except KeyboardInterrupt:
            print(Fore.YELLOW + "\nĐang dừng bot..." + Fore.RESET)
            shutdown_msg = self.config.get('messages', {}).get('shutdown', 'ĐÃ OFFLINE! 👋')
            self.send_message(f"{bot_name} {shutdown_msg}")
        except Exception as e:
            print(Fore.RED + f"Chat listener error: {e}" + Fore.RESET)
            logging.error(f"Chat listener error: {e}")

def start_bot():
    """Initialize and start the bot"""
    # Ensure logs directory exists
    import os
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    bot = YouTubeChatBot()
    
    # Authenticate
    if not bot.authenticate():
        return
    
    # Get stream URL
    url = bot.get_live_stream_url()
    video_id = bot.extract_video_id(url)
    
    if not video_id:
        print(Fore.RED + "Invalid YouTube URL!" + Fore.RESET)
        return
    
    bot.video_id = video_id
    print(Fore.GREEN + f"✓ Video ID: {video_id}" + Fore.RESET)
    
    # Get live chat ID
    live_chat_id = bot.get_live_chat_id(video_id)
    
    if not live_chat_id:
        print(Fore.RED + "Could not find active live chat!" + Fore.RESET)
        print(Fore.YELLOW + "Make sure the stream is live." + Fore.RESET)
        return
    
    bot.live_chat_id = live_chat_id
    print(Fore.GREEN + f"✓ Connected to live chat!" + Fore.RESET)
    
    # Start listening
    bot.start_chat_listener()
