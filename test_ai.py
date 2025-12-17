"""
Test AI Bot - Gemini và Ollama
Kiểm tra cả hai handler với các test case đa dạng
"""
from colorama import init, Fore
import json

init(autoreset=True)

def test_ai_handler(handler_name, handler):
    """Test một AI handler với các test cases"""
    print(Fore.CYAN + f"\n{'='*70}" + Fore.RESET)
    print(Fore.CYAN + f"Testing: {handler_name}" + Fore.RESET)
    print(Fore.CYAN + f"{'='*70}\n" + Fore.RESET)
    
    test_cases = [
        {
            "query": "ACN là ai?",
            "type": "Có trong knowledge",
            "expect_rag": True
        },
        {
            "query": "ACN tên thật là gì?",
            "type": "Có trong knowledge",
            "expect_rag": True
        },
        {
            "query": "lời khuyên của ACN",
            "type": "Có trong knowledge",
            "expect_rag": True
        },
        {
            "query": "Saitama vs Goku ai mạnh hơn?",
            "type": "Không có trong knowledge",
            "expect_rag": False
        },
        {
            "query": "Python là gì?",
            "type": "Không có trong knowledge",
            "expect_rag": False
        },
    ]
    
    passed = 0
    failed = 0
    
    for i, test in enumerate(test_cases, 1):
        query = test["query"]
        test_type = test["type"]
        expect_rag = test["expect_rag"]
        
        print(f"{Fore.YELLOW}Test {i}/{len(test_cases)}: {test_type}{Fore.RESET}")
        print(f"  Câu hỏi: {query}")
        
        try:
            response = handler.get_response(query, "TestUser")
            
            # Kiểm tra response
            has_response = bool(response and len(response) > 0)
            no_mentions = '@' not in response
            proper_length = len(response) <= 200
            
            print(f"  {Fore.GREEN}✓ Trả lời: {response[:100]}...{Fore.RESET}")
            print(f"  Độ dài: {len(response)} ký tự")
            
            # Validate
            checks = []
            if has_response:
                checks.append(f"{Fore.GREEN}✓ Có response{Fore.RESET}")
            else:
                checks.append(f"{Fore.RED}✗ Không có response{Fore.RESET}")
                
            if no_mentions:
                checks.append(f"{Fore.GREEN}✓ Không có @ mention{Fore.RESET}")
            else:
                checks.append(f"{Fore.RED}✗ Có @ mention{Fore.RESET}")
                
            if proper_length:
                checks.append(f"{Fore.GREEN}✓ Độ dài OK (<200){Fore.RESET}")
            else:
                checks.append(f"{Fore.RED}✗ Quá dài (>{200}){Fore.RESET}")
            
            print(f"  {' | '.join(checks)}")
            
            if has_response and no_mentions and proper_length:
                passed += 1
                print(f"  {Fore.GREEN}✓ PASS{Fore.RESET}")
            else:
                failed += 1
                print(f"  {Fore.RED}✗ FAIL{Fore.RESET}")
                
        except Exception as e:
            failed += 1
            print(f"  {Fore.RED}✗ Error: {e}{Fore.RESET}")
            print(f"  {Fore.RED}✗ FAIL{Fore.RESET}")
        
        print()
    
    # Summary
    total = len(test_cases)
    print(Fore.CYAN + f"{'='*70}" + Fore.RESET)
    print(f"{Fore.CYAN}Kết quả: {Fore.GREEN}{passed}/{total} PASS{Fore.RESET} | {Fore.RED}{failed}/{total} FAIL{Fore.RESET}")
    print(Fore.CYAN + f"{'='*70}\n" + Fore.RESET)
    
    return passed, failed

def main():
    print(Fore.CYAN + "╔" + "═"*68 + "╗" + Fore.RESET)
    print(Fore.CYAN + "║" + " "*20 + "AI BOT TEST SUITE" + " "*32 + "║" + Fore.RESET)
    print(Fore.CYAN + "╚" + "═"*68 + "╝" + Fore.RESET)
    
    # Load config
    with open('config/bot_config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    ai_config = config.get('ai', {})
    provider = ai_config.get('provider', 'gemini')
    
    print(f"\n{Fore.YELLOW}Provider hiện tại: {provider}{Fore.RESET}\n")
    
    # Test based on provider
    if provider == 'ollama':
        print(Fore.GREEN + "Testing Ollama Handler..." + Fore.RESET)
        from app.ollama_handler import OllamaHandler
        
        model = ai_config.get('ollama_model', 'llama3')
        host = ai_config.get('ollama_host', 'http://localhost:11434')
        
        handler = OllamaHandler(model=model, host=host)
        passed, failed = test_ai_handler("Ollama", handler)
        
    else:  # gemini
        print(Fore.GREEN + "Testing Gemini Handler..." + Fore.RESET)
        from app.ai_handler import GeminiMultiKeyHandler
        
        handler = GeminiMultiKeyHandler(ai_config)
        passed, failed = test_ai_handler("Gemini", handler)
    
    # Final summary
    print(Fore.CYAN + "\n" + "╔" + "═"*68 + "╗" + Fore.RESET)
    print(Fore.CYAN + "║" + " "*25 + "FINAL RESULT" + " "*31 + "║" + Fore.RESET)
    print(Fore.CYAN + "╚" + "═"*68 + "╝" + Fore.RESET)
    
    if failed == 0:
        print(Fore.GREEN + f"\n🎉 ALL TESTS PASSED! ({passed} tests)" + Fore.RESET)
    else:
        print(Fore.YELLOW + f"\n⚠ {passed} passed, {failed} failed" + Fore.RESET)
    
    print()

if __name__ == "__main__":
    main()
