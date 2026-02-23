import sys
import time

def main():
    try:
        import pytchat
    except Exception as e:
        print(f"ERROR: Could not import pytchat: {e}")
        sys.exit(1)

    video_id = sys.argv[1] if len(sys.argv) > 1 else "uIx8l2xlYVY"
    print(f"Using pytchat.create on video_id={video_id}")
    try:
        chat = pytchat.create(video_id=video_id)
    except Exception as e:
        print(f"ERROR: pytchat.create failed: {e}")
        sys.exit(2)

    # Doc-style loop
    while chat.is_alive():
        for c in chat.get().sync_items():
            print(f"{c.datetime} [{c.author.name}]- {c.message}")
        time.sleep(0.2)

if __name__ == "__main__":
    main()
