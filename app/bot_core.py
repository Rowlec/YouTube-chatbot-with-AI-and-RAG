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
        self.auto_message_interval = 180  # 3 minutes in seconds
        # Pytchat fallback/retry controls
        self.pytchat_retry_interval = int(self.config.get('pytchat_retry_sec', 90))
        self.last_pytchat_retry = time.time()
        self.pytchat_cookies = self.config.get('pytchat_cookies', '')
        
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

    def get_active_live_video_id(self, channel_id: str) -> Optional[str]:
        """Try to detect the currently active live video for a given channel"""
        try:
            req = self.youtube.search().list(
                part="id",
                channelId=channel_id,
                eventType="live",
                type="video",
                maxResults=1
            )
            resp = req.execute()
            items = resp.get('items', [])
            if items:
                vid = items[0].get('id', {}).get('videoId')
                if vid:
                    logging.info(f"Detected active live video for channel {channel_id}: {vid}")
                    return vid
            logging.info(f"No active live video found for channel {channel_id}")
            return None
        except Exception as e:
            logging.error(f"Active live video detection error: {e}")
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
        """Send periodic promotional messages every 3 minutes"""
        current_time = time.time()
        
        if current_time - self.last_auto_message_time >= self.auto_message_interval:
            import random
            messages = [
                "Tham gia cộng đồng discord của ACN tại đây: discord.gg/acn 🎮💬",
                "Mọi người có thể sử dụng lệnh !ask <Câu hỏi> để trò chuyện với bot nhé <3 🤖✨",
                "Anh em nhớ làm theo lời khuyên của ACN: \"Hãy làm người thật tốt\" 🗿🗿💙",
                "Mọi người có thể ủng hộ người làm ra bot (Rowlec) tại đây: stk: 103879245411 ngân hàng: VIETINBANK họ tên: LE NHUT ANH, xin chân thành cảm ơn 🙏💖",
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
        
        # Try to open pytchat; prefer LiveChat (doc-style) first, then create() as backup.
        chat = None
        try:
            chat = pytchat.LiveChat(video_id=self.video_id)
            logging.info(f"Initialized pytchat LiveChat for video_id={self.video_id}")
        except Exception as e_live:
            logging.info(f"LiveChat init failed: {e_live}. Will try create() next.")
            try:
                # Prefer full chat (not TopChat) and pass cookies if configured
                if self.pytchat_cookies:
                    chat = pytchat.create(video_id=self.video_id, topchat_only=False, cookies=self.pytchat_cookies)
                else:
                    chat = pytchat.create(video_id=self.video_id, topchat_only=False)
                logging.info(f"Initialized pytchat create() for video_id={self.video_id}")
            except Exception as e_create:
                logging.error(f"Failed to init pytchat (LiveChat & create) for video_id={self.video_id}: {e_create}")
                print(Fore.YELLOW + "⚠ Không thể dùng pytchat cho video này. Sẽ chuyển sang đọc chat bằng YouTube Data API." + Fore.RESET)
        
        try:
            # If pytchat is alive, read from it; otherwise fall back to API.
            if chat is not None and chat.is_alive():
                while chat.is_alive():
                    # Send periodic messages
                    self.send_periodic_messages()
                    data = chat.get()
                    # Use sync_items if available (create()), otherwise items (LiveChat)
                    try:
                        items_fn = getattr(data, 'sync_items', None)
                        items = items_fn() if callable(items_fn) else data.items
                    except Exception:
                        items = getattr(data, 'items', [])
                    for chat_item in items:
                        self.process_message(chat_item)
                    time.sleep(0.1)

            # Fallback: poll messages via YouTube Data API (also if pytchat died)
            if chat is None or not chat.is_alive():
                next_page_token = None
                while True:
                    self.send_periodic_messages()
                    try:
                        resp = self.youtube.liveChatMessages().list(
                            liveChatId=self.live_chat_id,
                            part="snippet,authorDetails",
                            pageToken=next_page_token,
                            maxResults=200
                        ).execute()
                        items = resp.get('items', [])
                        next_page_token = resp.get('nextPageToken')
                        for item in items:
                            chat_item = self._convert_api_item(item)
                            if chat_item:
                                self.process_message(chat_item)
                        # Use polling interval from API if available
                        wait_ms = resp.get('pollingIntervalMillis', 2000)
                        time.sleep(wait_ms / 1000.0)
                        # Periodically retry switching back to pytchat
                        if time.time() - self.last_pytchat_retry >= self.pytchat_retry_interval:
                            self.last_pytchat_retry = time.time()
                            try:
                                # Try LiveChat first
                                chat = None
                                try:
                                    chat = pytchat.LiveChat(video_id=self.video_id)
                                    logging.info("Retry: LiveChat connected")
                                except Exception as retry_live_err:
                                    logging.info(f"Retry LiveChat failed: {retry_live_err}. Trying create().")
                                    try:
                                        if self.pytchat_cookies:
                                            chat = pytchat.create(video_id=self.video_id, topchat_only=False, cookies=self.pytchat_cookies)
                                        else:
                                            chat = pytchat.create(video_id=self.video_id, topchat_only=False)
                                        logging.info("Retry: create() connected")
                                    except Exception as retry_create_err:
                                        logging.info(f"Retry create() still failing: {retry_create_err}")
                                if chat is not None:
                                    print(Fore.GREEN + "✓ Đã chuyển lại sang pytchat (ít tốn quota hơn)." + Fore.RESET)
                                    # Drain existing API loop then switch to pytchat loop
                                    while chat.is_alive():
                                        self.send_periodic_messages()
                                        data = chat.get()
                                        try:
                                            items_fn = getattr(data, 'sync_items', None)
                                            items = items_fn() if callable(items_fn) else data.items
                                        except Exception:
                                            items = getattr(data, 'items', [])
                                        for chat_item in items:
                                            self.process_message(chat_item)
                                        time.sleep(0.1)
                            except Exception as re_try_e:
                                logging.info(f"Retry pytchat still failing: {re_try_e}")
                    except Exception as api_e:
                        logging.error(f"Data API chat poll error: {api_e}")
                        time.sleep(2.0)
        except KeyboardInterrupt:
            print(Fore.YELLOW + "\nĐang dừng bot..." + Fore.RESET)
            shutdown_msg = self.config.get('messages', {}).get('shutdown', 'ĐÃ OFFLINE! 👋')
            self.send_message(f"{bot_name} {shutdown_msg}")
        except Exception as e:
            print(Fore.RED + f"Chat listener error: {e}" + Fore.RESET)
            logging.error(f"Chat listener error: {e}")

    def _convert_api_item(self, item):
        """Convert YouTube Data API liveChatMessages item to a pytchat-like object"""
        try:
            author = item.get('authorDetails', {})
            snippet = item.get('snippet', {})
            class Author:
                def __init__(self, d):
                    self.channelId = d.get('channelId', '')
                    self.name = d.get('displayName', '')
                    self.isChatOwner = bool(d.get('isChatOwner', False))
                    self.isChatModerator = bool(d.get('isChatModerator', False))
                    self.isChatSponsor = bool(d.get('isChatSponsor', False))
            class ChatItem:
                def __init__(self, a, s):
                    self.author = a
                    self.message = s.get('displayMessage', '')
                    # Use publishedAt as timestamp, fallback to current time
                    pub = s.get('publishedAt')
                    self.timestamp = pub if pub else str(time.time())
                    # Human-readable datetime
                    try:
                        dt = datetime.fromisoformat(pub.replace('Z', '+00:00')) if pub else datetime.now()
                    except Exception:
                        dt = datetime.now()
                    self.datetime = dt.strftime('%Y-%m-%d %H:%M:%S')
            return ChatItem(Author(author), snippet)
        except Exception as e:
            logging.error(f"Convert API item error: {e}")
            return None

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
