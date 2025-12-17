"""
Moderation Handler
Handles spam detection, emoji limits, word limits, and timeouts
"""
import emoji
import logging
from collections import defaultdict
from colorama import Fore

class ModerationHandler:
    def __init__(self, bot):
        self.bot = bot
        self.user_messages = defaultdict(list)  # Track user messages for spam detection
        
    def check_message(self, chat_item) -> dict:
        """
        Check message for moderation issues
        Returns dict with 'allowed' bool and optional 'reason'
        """
        author = chat_item.author
        message = chat_item.message
        
        # Skip checks for owner
        if author.isChatOwner:
            return {'allowed': True}
        
        # Check emoji spam
        if not self.check_emoji_limit(author, message):
            return {'allowed': False, 'reason': 'emoji_spam'}
        
        # Check word spam
        if not self.check_word_spam(author, message):
            return {'allowed': False, 'reason': 'word_spam'}
        
        # Check message spam (repeated messages)
        if not self.check_message_spam(author, message):
            return {'allowed': False, 'reason': 'message_spam'}
        
        # Check for links (optional, can be enabled in config)
        # if self.has_links(message):
        #     return {'allowed': False, 'reason': 'links'}
        
        return {'allowed': True}
    
    def check_emoji_limit(self, author, message: str) -> bool:
        """Check if message has too many emojis"""
        emoji_limit = self.bot.config['moderation'].get('emoji_limit', 5)
        
        # Count emojis
        emoji_count = emoji.emoji_count(message)
        
        if emoji_count > emoji_limit:
            timeout_duration = self.get_timeout_duration(author)
            self.timeout_user_with_message(
                author,
                timeout_duration,
                f"Vui lòng không spam emoji (giới hạn: {emoji_limit})"
            )
            return False
        
        return True
    
    def check_word_spam(self, author, message: str) -> bool:
        """Check for repeated words in message"""
        word_limit = self.bot.config['moderation'].get('word_limit', 3)
        
        words = message.lower().split()
        word_counts = {}
        
        for word in words:
            # Skip very short words and emojis
            if len(word) <= 2 or word.startswith(':'):
                continue
            
            word_counts[word] = word_counts.get(word, 0) + 1
            
            if word_counts[word] > word_limit:
                timeout_duration = self.get_timeout_duration(author)
                self.timeout_user_with_message(
                    author,
                    timeout_duration,
                    f"Vui lòng không spam cùng một từ"
                )
                return False
        
        return True
    
    def check_message_spam(self, author, message: str) -> bool:
        """Check for repeated messages from same user"""
        channel_id = author.channelId
        
        # Keep track of last 5 messages per user
        self.user_messages[channel_id].append(message.lower())
        if len(self.user_messages[channel_id]) > 5:
            self.user_messages[channel_id].pop(0)
        
        # Check if user is sending same message repeatedly
        recent_messages = self.user_messages[channel_id]
        if len(recent_messages) >= 3:
            if recent_messages[-1] == recent_messages[-2] == recent_messages[-3]:
                timeout_duration = self.get_timeout_duration(author)
                self.timeout_user_with_message(
                    author,
                    timeout_duration,
                    "Vui lòng không spam cùng một tin nhắn"
                )
                # Clear their message history
                self.user_messages[channel_id].clear()
                return False
        
        return True
    
    def has_links(self, message: str) -> bool:
        """Check if message contains links"""
        link_indicators = ['http://', 'https://', 'www.', '.com', '.net', '.org']
        message_lower = message.lower()
        return any(indicator in message_lower for indicator in link_indicators)
    
    def get_timeout_duration(self, author) -> int:
        """Get timeout duration based on user type"""
        if author.isChatModerator:
            return self.bot.config['moderation'].get('timeout_mod', 60)
        else:
            return self.bot.config['moderation'].get('timeout_normal', 300)
    
    def timeout_user_with_message(self, author, duration: int, reason: str):
        """Timeout user and send message"""
        minutes = duration // 60
        seconds = duration % 60
        
        time_str = f"{minutes} phút {seconds} giây" if minutes > 0 else f"{seconds} giây"
        
        user_type = ""
        if author.isChatModerator:
            user_type = " (Moderator)"
        
        message = f"@{author.name}{user_type} {reason}. [Timeout: {time_str}]"
        
        print(Fore.YELLOW + f"⚠ Timeout: {author.name} - {reason}" + Fore.RESET)
        logging.warning(f"Timeout: {author.name} ({author.channelId}) - {reason} - {duration}s")
        
        self.bot.send_message(message)
        self.bot.timeout_user(author.channelId, duration)
