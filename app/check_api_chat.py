import sys
import time
import os

def main():
    from colorama import Fore
    # Ensure workspace root is on sys.path so 'app' package is importable
    workspace_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    if workspace_root not in sys.path:
        sys.path.append(workspace_root)
    from app.bot_core import YouTubeChatBot

    if len(sys.argv) < 2:
        print("Usage: python app/check_api_chat.py <video_id>")
        sys.exit(2)

    video_id = sys.argv[1]
    bot = YouTubeChatBot()
    if not bot.authenticate():
        sys.exit(1)

    print(Fore.CYAN + f"Checking Data API for video: {video_id}" + Fore.RESET)
    chat_id = bot.get_live_chat_id(video_id)
    if not chat_id:
        print(Fore.YELLOW + "No activeLiveChatId found. Stream may be offline or restricted." + Fore.RESET)
        sys.exit(3)

    print(Fore.GREEN + f"✓ activeLiveChatId: {chat_id}" + Fore.RESET)
    bot.live_chat_id = chat_id

    try:
        resp = bot.youtube.liveChatMessages().list(
            liveChatId=chat_id,
            part="snippet,authorDetails",
            maxResults=50
        ).execute()
        items = resp.get('items', [])
        if not items:
            print(Fore.YELLOW + "No messages returned in first page." + Fore.RESET)
            sys.exit(4)
        print(Fore.GREEN + f"✓ Received {len(items)} messages from API." + Fore.RESET)
        # Print a few
        for item in items[:5]:
            author = item.get('authorDetails', {}).get('displayName', '?')
            message = item.get('snippet', {}).get('displayMessage', '')
            print(f"{author}: {message}")
    except Exception as e:
        print(Fore.RED + f"Error fetching messages: {e}" + Fore.RESET)
        sys.exit(5)

if __name__ == "__main__":
    main()
