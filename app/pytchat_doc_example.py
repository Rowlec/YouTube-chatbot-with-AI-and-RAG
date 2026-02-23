import sys
import time

def run_create(video_id: str, duration_sec: int = 20):
    import pytchat
    chat = pytchat.create(video_id=video_id)
    start = time.time()
    while chat.is_alive() and (time.time() - start) < duration_sec:
        for c in chat.get().sync_items():
            print(f"{c.author.name}: {c.message}")
        time.sleep(0.2)

def run_livechat(video_id: str, duration_sec: int = 20):
    import pytchat
    chat = pytchat.LiveChat(video_id=video_id)
    start = time.time()
    while chat.is_alive() and (time.time() - start) < duration_sec:
        chatdata = chat.get()
        for c in chatdata.items:
            print(f"{c.author.name}: {c.message}")
        time.sleep(0.2)

def main():
    if len(sys.argv) < 2:
        print("Usage: python app/pytchat_doc_example.py <video_id>")
        sys.exit(2)
    vid = sys.argv[1]
    try:
        print("Trying pytchat.create (doc style)...")
        run_create(vid)
        print("Done create().")
    except Exception as e:
        print(f"create() failed: {e}")
        try:
            print("Trying pytchat.LiveChat (alternate doc style)...")
            run_livechat(vid)
            print("Done LiveChat.")
        except Exception as e2:
            print(f"LiveChat failed: {e2}")
            sys.exit(1)

if __name__ == "__main__":
    main()
