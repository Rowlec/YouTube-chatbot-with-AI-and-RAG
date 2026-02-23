import sys
import os

def main():
    from colorama import Fore
    # Ensure workspace root in path
    workspace_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    if workspace_root not in sys.path:
        sys.path.append(workspace_root)
    from app.bot_core import YouTubeChatBot

    if len(sys.argv) < 2:
        print("Usage: python app/check_video_flags.py <video_id>")
        sys.exit(2)

    vid = sys.argv[1]
    bot = YouTubeChatBot()
    if not bot.authenticate():
        sys.exit(1)

    try:
        resp = bot.youtube.videos().list(
            part="snippet,liveStreamingDetails,status,contentDetails",
            id=vid
        ).execute()
        items = resp.get('items', [])
        if not items:
            print(Fore.RED + "No video found for that ID." + Fore.RESET)
            sys.exit(3)
        v = items[0]
        status = v.get('status', {})
        content = v.get('contentDetails', {})
        live = v.get('liveStreamingDetails', {})
        snippet = v.get('snippet', {})
        print(Fore.CYAN + "Video flags:" + Fore.RESET)
        print(f" - title: {snippet.get('title','')}\n - privacyStatus: {status.get('privacyStatus')}\n - madeForKids: {status.get('madeForKids')}\n - selfDeclaredMadeForKids: {status.get('selfDeclaredMadeForKids')}\n - uploadStatus: {status.get('uploadStatus')}\n - regionRestriction.allowed: {content.get('regionRestriction',{}).get('allowed')}\n - regionRestriction.blocked: {content.get('regionRestriction',{}).get('blocked')}\n - contentRating: {content.get('contentRating')}\n - activeLiveChatId?: {bool(live.get('activeLiveChatId'))}\n - concurrentViewers: {live.get('concurrentViewers')}\n - actualStartTime: {live.get('actualStartTime')}\n - scheduledStartTime: {live.get('scheduledStartTime')}\n")
    except Exception as e:
        print(Fore.RED + f"Error fetching video flags: {e}" + Fore.RESET)
        sys.exit(4)

if __name__ == "__main__":
    main()
