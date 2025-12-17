"""
YouTube Live Chat Bot
Main entry point for the bot application
"""
import os
import sys
from colorama import init, Fore
from app.bot_core import start_bot

def clear_screen():
    """Clear terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    """Main function to initialize and start the bot"""
    # Initialize colorama for colored terminal output
    init()
    
    # Clear screen
    clear_screen()
    
    # Display banner
    print(Fore.CYAN + "=" * 50)
    print(Fore.GREEN + "    YouTube Live Chat Bot")
    print(Fore.CYAN + "=" * 50 + Fore.RESET)
    print()
    
    # Start the bot
    try:
        start_bot()
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n\nBot stopped by user." + Fore.RESET)
    except Exception as e:
        print(Fore.RED + f"\n\nCritical error: {e}" + Fore.RESET)
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
