"""
Test RAG Knowledge Base Matching
Kiểm tra xem RAG có tìm được context phù hợp không
"""
from app.rag_handler import RAGKnowledgeBase
from colorama import Fore, init

init(autoreset=True)

def test_query(rag, query):
    """Test a single query"""
    print(f"\n{Fore.CYAN}Query: {query}{Fore.RESET}")
    results = rag.search(query, top_k=3)
    
    if results:
        print(f"{Fore.GREEN}✓ Found {len(results)} matches:{Fore.RESET}")
        for i, result in enumerate(results, 1):
            print(f"  {i}. Score: {result['score']}")
            print(f"     Keywords: {result['matched_keywords']}")
            print(f"     Content: {result['content'][:100]}...")
    else:
        print(f"{Fore.RED}✗ No matches found{Fore.RESET}")

def main():
    print(f"{Fore.YELLOW}=== RAG Knowledge Base Test ==={Fore.RESET}\n")
    
    # Initialize RAG
    rag = RAGKnowledgeBase('config/knowledge.json')
    print(f"Loaded {len(rag.knowledge)} knowledge entries\n")
    
    # Test queries
    test_queries = [
        "ACN là ai?",
        "ACN làm content gì?",
        "Discord của ACN",
        "ai làm bot này",
        "lời khuyên của ACN",
        "ACN bao nhiêu tuổi",
        "sinh nhật ACN khi nào",
        "tên thật của ACN",
        "Rowlec là ai",
        "mẹ kct",
        "ACN chơi game gì",
        "discord.gg/acn",
        "công ty ACN",
        "ACN cao bao nhiêu",
    ]
    
    for query in test_queries:
        test_query(rag, query)
    
    print(f"\n{Fore.YELLOW}=== Test Complete ==={Fore.RESET}")

if __name__ == "__main__":
    main()
