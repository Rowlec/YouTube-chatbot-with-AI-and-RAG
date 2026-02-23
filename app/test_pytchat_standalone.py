#!/usr/bin/env python
"""
Standalone pytchat tester - validate pytchat on archived/past livestream videos
"""
import sys
import time

def test_livechat(video_id: str, timeout_sec: int = 15):
    """Test pytchat.LiveChat method"""
    print(f"\n[Test] pytchat.LiveChat on {video_id}")
    try:
        import pytchat
        chat = pytchat.LiveChat(video_id=video_id)
        print(f"  ✓ LiveChat initialized, is_alive={chat.is_alive()}")
        
        if not chat.is_alive():
            print(f"  ⚠ LiveChat not alive (stream may be offline/archived)")
            return False
        
        start = time.time()
        msg_count = 0
        while chat.is_alive() and (time.time() - start) < timeout_sec:
            try:
                data = chat.get()
                if hasattr(data, 'items'):
                    for item in data.items:
                        author = getattr(item.author, 'name', '?')
                        message = getattr(item, 'message', '')
                        print(f"    [{author}] {message[:60]}")
                        msg_count += 1
                        if msg_count >= 5:
                            print(f"  ✓ LiveChat SUCCESS: Read {msg_count} messages")
                            return True
            except Exception as e:
                print(f"    Error reading: {e}")
            time.sleep(0.2)
        
        if msg_count > 0:
            print(f"  ✓ LiveChat SUCCESS: Read {msg_count} messages")
            return True
        else:
            print(f"  ✗ LiveChat: No messages received (stream may be offline)")
            return False
    except Exception as e:
        print(f"  ✗ LiveChat FAILED: {e}")
        return False

def test_create(video_id: str, timeout_sec: int = 15):
    """Test pytchat.create method"""
    print(f"\n[Test] pytchat.create on {video_id}")
    try:
        import pytchat
        chat = pytchat.create(video_id=video_id)
        print(f"  ✓ create() initialized, is_alive={chat.is_alive()}")
        
        if not chat.is_alive():
            print(f"  ⚠ create() not alive (stream may be offline/archived)")
            return False
        
        start = time.time()
        msg_count = 0
        while chat.is_alive() and (time.time() - start) < timeout_sec:
            try:
                data = chat.get()
                for item in data.sync_items():
                    author = getattr(item.author, 'name', '?')
                    message = getattr(item, 'message', '')
                    print(f"    [{author}] {message[:60]}")
                    msg_count += 1
                    if msg_count >= 5:
                        print(f"  ✓ create() SUCCESS: Read {msg_count} messages")
                        return True
            except Exception as e:
                print(f"    Error reading: {e}")
            time.sleep(0.2)
        
        if msg_count > 0:
            print(f"  ✓ create() SUCCESS: Read {msg_count} messages")
            return True
        else:
            print(f"  ✗ create(): No messages received (stream may be offline)")
            return False
    except Exception as e:
        print(f"  ✗ create() FAILED: {e}")
        return False

def main():
    if len(sys.argv) < 2:
        print("Usage: python app/test_pytchat_standalone.py <video_id>")
        print("\nExample video IDs to test (past livestreams with saved chat):")
        print("  YpF_s0QqP6o")
        print("  uIx8l2xlYVY")
        print("\nNote: Pytchat only works on videos with active/saved chat.")
        print("      Past livestreams usually have chat data available.")
        sys.exit(2)
    
    vid = sys.argv[1]
    print(f"Testing pytchat on video: {vid}")
    print("=" * 60)
    
    # Try both methods
    livechat_ok = test_livechat(vid, timeout_sec=15)
    create_ok = test_create(vid, timeout_sec=15)
    
    # Summary
    print("\n" + "=" * 60)
    print("[Summary]")
    print(f"  LiveChat: {'✓ WORKS' if livechat_ok else '✗ FAILED'}")
    print(f"  create():  {'✓ WORKS' if create_ok else '✗ FAILED'}")
    
    if livechat_ok or create_ok:
        print(f"\n✓ Pytchat can read chat from this video!")
        sys.exit(0)
    else:
        print(f"\n✗ Pytchat cannot read chat from this video.")
        print("   This is likely because:")
        print("   - Video doesn't have chat enabled or is very old")
        print("   - Stream was unlisted/private")
        print("   - YouTube blocked pytchat's access (markup changed)")
        sys.exit(1)

if __name__ == "__main__":
    main()
