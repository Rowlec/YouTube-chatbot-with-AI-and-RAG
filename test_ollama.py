"""
Test Ollama Handler
Kiểm tra xem Ollama có hoạt động đúng không
"""
from app.ollama_handler import OllamaHandler
from app.rag_handler import RAGKnowledgeBase
from colorama import init, Fore

init(autoreset=True)

def test_ollama():
    print(Fore.CYAN + "=== Test Ollama Handler ===" + Fore.RESET)
    
    # Initialize handler
    model = "llama3"
    host = "http://localhost:11434"
    
    print(Fore.YELLOW + f"Khởi tạo Ollama Handler (Model: {model}, Host: {host})" + Fore.RESET)
    handler = OllamaHandler(model=model, host=host)
    
    # Initialize RAG
    print(Fore.YELLOW + "Khởi tạo RAG Knowledge Base..." + Fore.RESET)
    rag = RAGKnowledgeBase('config/knowledge.json')
    print(Fore.GREEN + f"✓ Loaded {len(rag.knowledge)} knowledge entries" + Fore.RESET)
    
    # Test cases
    test_cases = [
        {
            "query": "ACN là ai?",
            "description": "Câu hỏi CÓ trong knowledge base"
        },
        {
            "query": "ACN tên thật là gì?",
            "description": "Câu hỏi CÓ trong knowledge base"
        },
        {
            "query": "ACN bao nhiêu tuổi?",
            "description": "Câu hỏi CÓ trong knowledge base"
        },
        {
            "query": "lời khuyên của ACN là gì?",
            "description": "Câu hỏi CÓ trong knowledge base"
        },
        {
            "query": "Saitama vs Goku ai mạnh hơn?",
            "description": "Câu hỏi KHÔNG có trong knowledge base"
        },
        {
            "query": "Justin Bieber là ai?",
            "description": "Câu hỏi KHÔNG có trong knowledge base"
        },
    ]
    
    print("\n" + Fore.CYAN + "=" * 60 + Fore.RESET)
    
    for i, test in enumerate(test_cases, 1):
        query = test["query"]
        description = test["description"]
        
        print(f"\n{Fore.YELLOW}Test {i}: {description}{Fore.RESET}")
        print(f"{Fore.WHITE}Câu hỏi: {query}{Fore.RESET}")
        
        # Get context from RAG
        context = rag.get_context(query, max_length=300)
        
        if context:
            print(f"{Fore.GREEN}✓ RAG tìm thấy context{Fore.RESET}")
            print(f"{Fore.CYAN}Context: {context[:100]}...{Fore.RESET}")
        else:
            print(f"{Fore.RED}✗ RAG không tìm thấy context{Fore.RESET}")
        
        # Get response from Ollama
        response = handler.get_response(query, user_name="TestUser", context=context)
        
        print(f"{Fore.GREEN}Trả lời: {response}{Fore.RESET}")
        print(f"{Fore.MAGENTA}Độ dài: {len(response)} ký tự{Fore.RESET}")
        
        # Kiểm tra có @ mention không
        if '@' in response:
            print(f"{Fore.RED}⚠ Cảnh báo: Phát hiện @ mention trong câu trả lời!{Fore.RESET}")
        else:
            print(f"{Fore.GREEN}✓ Không có @ mention{Fore.RESET}")
        
        # Kiểm tra độ dài
        if len(response) > 200:
            print(f"{Fore.RED}⚠ Cảnh báo: Câu trả lời quá dài (>{200} ký tự)!{Fore.RESET}")
        else:
            print(f"{Fore.GREEN}✓ Độ dài phù hợp (<200 ký tự){Fore.RESET}")
        
        print(Fore.CYAN + "-" * 60 + Fore.RESET)
    
    print(f"\n{Fore.CYAN}=== Test hoàn tất! ==={Fore.RESET}")

if __name__ == "__main__":
    test_ollama()
