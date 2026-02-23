import sys
import time

def main():
    try:
        import pytchat
    except Exception as e:
        print(f"ERROR: Failed to import pytchat: {e}")
        sys.exit(1)

    if len(sys.argv) < 2:
        print("Usage: python app/check_chat.py <video_id>")
        sys.exit(2)

    video_id = sys.argv[1]
    print(f"Checking live chat for video: {video_id}")

    try:
        chat = pytchat.create(video_id=video_id, topchat_only=False)
    except Exception as e:
        print(f"ERROR: Unable to create pytchat stream: {e}")
        sys.exit(3)

    start = time.time()
    messages = 0
    max_messages = 10
    timeout_sec = 20

    try:
        while chat.is_alive() and (time.time() - start) < timeout_sec and messages < max_messages:
            data = chat.get()
            for item in data.items:
                # Basic fields available in pytchat item
                author = getattr(item.author, "name", "?")
                message = getattr(item, "message", "")
                timestamp = getattr(item, "timestamp", "")
                print(f"[{timestamp}] {author}: {message}")
                messages += 1
                if messages >= max_messages:
                    break
            # Small sleep to avoid tight loop
            time.sleep(0.5)
    except Exception as e:
        print(f"ERROR: Exception while reading chat: {e}")
        sys.exit(4)

    if messages == 0:
        print("No messages received within timeout. Stream may be offline or restricted.")
        sys.exit(5)
    else:
        print(f"Received {messages} messages.")

if __name__ == "__main__":
    main()
