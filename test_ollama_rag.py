"""
Test Ollama Handler with RAG Integration
20 comprehensive test cases for Ollama AI with RAG knowledge base
"""
import sys
import time
from colorama import Fore, init
from app.ollama_handler import OllamaHandler
from app.rag_handler import RAGKnowledgeBase

# Initialize colorama
init(autoreset=True)

class OllamaRAGTester:
    def __init__(self):
        """Initialize the tester with Ollama and RAG handlers"""
        print(Fore.CYAN + "=" * 80)
        print(Fore.CYAN + "OLLAMA + RAG INTEGRATION TEST SUITE (20 TEST CASES)")
        print(Fore.CYAN + "=" * 80 + "\n")
        
        # Configuration
        self.model = "gemma2:latest"  # Thay đổi từ llama3.2:latest sang gemma2:latest
        self.host = "http://localhost:11434"
        
        # Initialize handlers
        print(Fore.YELLOW + "Initializing Ollama Handler..." + Fore.RESET)
        try:
            self.ollama = OllamaHandler(model=self.model, host=self.host)
            print(Fore.GREEN + f"✓ Ollama Handler initialized (Model: {self.model})" + Fore.RESET)
        except Exception as e:
            print(Fore.RED + f"✗ Failed to initialize Ollama: {e}" + Fore.RESET)
            sys.exit(1)
        
        print(Fore.YELLOW + "\nInitializing RAG Knowledge Base..." + Fore.RESET)
        try:
            self.rag = RAGKnowledgeBase('config/knowledge.json')
            print(Fore.GREEN + f"✓ RAG Knowledge Base loaded: {len(self.rag.knowledge)} entries" + Fore.RESET)
        except Exception as e:
            print(Fore.RED + f"✗ Failed to initialize RAG: {e}" + Fore.RESET)
            sys.exit(1)
        
        self.test_results = []
        print()
    
    def run_test(self, test_number: int, test_name: str, query: str, should_have_rag: bool = True):
        """
        Run a single test case
        
        Args:
            test_number: Test case number
            test_name: Name/description of the test
            query: Query to test
            should_have_rag: Whether RAG context is expected
        """
        print(Fore.CYAN + f"\n{'=' * 80}")
        print(Fore.CYAN + f"TEST {test_number}/20: {test_name}")
        print(Fore.CYAN + f"{'=' * 80}")
        print(Fore.YELLOW + f"Query: {query}" + Fore.RESET)
        
        try:
            # Test RAG search
            print(Fore.MAGENTA + "\n[1] RAG Knowledge Search:" + Fore.RESET)
            rag_results = self.rag.search(query, top_k=3)
            
            if rag_results:
                print(Fore.GREEN + f"  ✓ Found {len(rag_results)} matching entries" + Fore.RESET)
                for i, result in enumerate(rag_results, 1):
                    print(Fore.WHITE + f"    {i}. Score: {result['score']}, Keywords: {result['matched_keywords']}" + Fore.RESET)
            else:
                print(Fore.YELLOW + "  ⚠ No RAG matches found" + Fore.RESET)
            
            # Test RAG context
            print(Fore.MAGENTA + "\n[2] RAG Context Generation:" + Fore.RESET)
            context = self.rag.get_context(query, max_length=300)
            
            if context:
                print(Fore.GREEN + f"  ✓ Context generated ({len(context)} chars)" + Fore.RESET)
                print(Fore.WHITE + f"  Context: {context[:150]}..." + Fore.RESET)
            else:
                print(Fore.YELLOW + "  ⚠ No context generated" + Fore.RESET)
            
            # Test Ollama response
            print(Fore.MAGENTA + "\n[3] Ollama AI Response:" + Fore.RESET)
            start_time = time.time()
            response = self.ollama.get_response(query, user_name="Tester")
            response_time = time.time() - start_time
            
            print(Fore.GREEN + f"  ✓ Response generated ({response_time:.2f}s)" + Fore.RESET)
            print(Fore.WHITE + f"  Response: {response}" + Fore.RESET)
            
            # Validate response
            print(Fore.MAGENTA + "\n[4] Response Validation:" + Fore.RESET)
            
            checks = {
                "Not empty": len(response.strip()) > 0,
                "Length <= 200 chars": len(response) <= 200,
                "Contains emoji": any(char for char in response if ord(char) > 127000),
                "Vietnamese text": any(c in response for c in ['ạ', 'ă', 'â', 'đ', 'ê', 'ô', 'ơ', 'ư']),
            }
            
            # Check RAG expectation
            if should_have_rag:
                checks["RAG context found"] = context is not None
            else:
                checks["No RAG needed"] = True
            
            all_passed = True
            for check_name, passed in checks.items():
                status = "✓" if passed else "✗"
                color = Fore.GREEN if passed else Fore.RED
                print(color + f"  {status} {check_name}" + Fore.RESET)
                if not passed:
                    all_passed = False
            
            # Record result
            self.test_results.append({
                'number': test_number,
                'name': test_name,
                'passed': all_passed,
                'rag_found': context is not None,
                'response_time': response_time
            })
            
            if all_passed:
                print(Fore.GREEN + f"\n✓ TEST {test_number} PASSED" + Fore.RESET)
            else:
                print(Fore.RED + f"\n✗ TEST {test_number} FAILED" + Fore.RESET)
            
        except Exception as e:
            print(Fore.RED + f"\n✗ TEST {test_number} ERROR: {e}" + Fore.RESET)
            self.test_results.append({
                'number': test_number,
                'name': test_name,
                'passed': False,
                'rag_found': False,
                'response_time': 0,
                'error': str(e)
            })
    
    def run_all_tests(self):
        """Run all 20 test cases"""
        
        # TEST CATEGORY 1: Basic ACN Information (Tests 1-5)
        print(Fore.YELLOW + "\n" + "=" * 80)
        print(Fore.YELLOW + "CATEGORY 1: BASIC ACN INFORMATION")
        print(Fore.YELLOW + "=" * 80)
        
        self.run_test(1, "ACN Identity Question", "ACN là ai?", should_have_rag=True)
        time.sleep(1)
        
        self.run_test(2, "ACN Content Type", "ACN làm video gì?", should_have_rag=True)
        time.sleep(1)
        
        self.run_test(3, "ACN Company Info", "ACN làm ở công ty nào?", should_have_rag=True)
        time.sleep(1)
        
        self.run_test(4, "ACN Channel Stats", "Kênh ACN có bao nhiêu sub?", should_have_rag=True)
        time.sleep(1)
        
        self.run_test(5, "ACN Location", "ACN ở đâu?", should_have_rag=True)
        time.sleep(1)
        
        # TEST CATEGORY 2: Community Links (Tests 6-8)
        print(Fore.YELLOW + "\n" + "=" * 80)
        print(Fore.YELLOW + "CATEGORY 2: COMMUNITY LINKS & SOCIAL MEDIA")
        print(Fore.YELLOW + "=" * 80)
        
        self.run_test(6, "Discord Link", "Link discord của ACN?", should_have_rag=True)
        time.sleep(1)
        
        self.run_test(7, "Facebook Link", "Facebook ACN là gì?", should_have_rag=True)
        time.sleep(1)
        
        self.run_test(8, "Donation Info", "Làm sao để donate cho ACN?", should_have_rag=True)
        time.sleep(1)
        
        # TEST CATEGORY 3: Gaming Content (Tests 9-11)
        print(Fore.YELLOW + "\n" + "=" * 80)
        print(Fore.YELLOW + "CATEGORY 3: GAMING CONTENT")
        print(Fore.YELLOW + "=" * 80)
        
        self.run_test(9, "Favorite Games", "ACN chơi game gì?", should_have_rag=True)
        time.sleep(1)
        
        self.run_test(10, "Minecraft Content", "ACN có chơi Minecraft không?", should_have_rag=True)
        time.sleep(1)
        
        self.run_test(11, "Gaming Setup", "Setup máy tính của ACN thế nào?", should_have_rag=True)
        time.sleep(1)
        
        # TEST CATEGORY 4: Personal Questions (Tests 12-14)
        print(Fore.YELLOW + "\n" + "=" * 80)
        print(Fore.YELLOW + "CATEGORY 4: PERSONAL INFORMATION")
        print(Fore.YELLOW + "=" * 80)
        
        self.run_test(12, "Age Question", "ACN bao nhiêu tuổi?", should_have_rag=True)
        time.sleep(1)
        
        self.run_test(13, "Real Name", "Tên thật của ACN là gì?", should_have_rag=True)
        time.sleep(1)
        
        self.run_test(14, "Relationship Status", "ACN có người yêu chưa?", should_have_rag=True)
        time.sleep(1)
        
        # TEST CATEGORY 5: General Knowledge (No RAG Expected) (Tests 15-17)
        print(Fore.YELLOW + "\n" + "=" * 80)
        print(Fore.YELLOW + "CATEGORY 5: GENERAL KNOWLEDGE (NO RAG)")
        print(Fore.YELLOW + "=" * 80)
        
        self.run_test(15, "General Greeting", "Xin chào bot!", should_have_rag=False)
        time.sleep(1)
        
        self.run_test(16, "General Question", "Hôm nay trời đẹp không?", should_have_rag=False)
        time.sleep(1)
        
        self.run_test(17, "Math Question", "2 + 2 bằng mấy?", should_have_rag=False)
        time.sleep(1)
        
        # TEST CATEGORY 6: Edge Cases & Complex Queries (Tests 18-20)
        print(Fore.YELLOW + "\n" + "=" * 80)
        print(Fore.YELLOW + "CATEGORY 6: EDGE CASES & COMPLEX QUERIES")
        print(Fore.YELLOW + "=" * 80)
        
        self.run_test(18, "Multi-Topic Query", "ACN làm gì và ở đâu?", should_have_rag=True)
        time.sleep(1)
        
        self.run_test(19, "Typo Handling", "Acn là aj?", should_have_rag=True)
        time.sleep(1)
        
        self.run_test(20, "Very Long Query", 
                     "Cho mình hỏi là kênh YouTube của ACN có bao nhiêu subscribers và ACN làm video về chủ đề gì vậy ạ?", 
                     should_have_rag=True)
    
    def print_summary(self):
        """Print test results summary"""
        print(Fore.CYAN + "\n" + "=" * 80)
        print(Fore.CYAN + "TEST SUMMARY")
        print(Fore.CYAN + "=" * 80 + "\n")
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for r in self.test_results if r['passed'])
        failed_tests = total_tests - passed_tests
        rag_used = sum(1 for r in self.test_results if r['rag_found'])
        avg_response_time = sum(r['response_time'] for r in self.test_results) / total_tests if total_tests > 0 else 0
        
        print(Fore.WHITE + f"Total Tests: {total_tests}")
        print(Fore.GREEN + f"Passed: {passed_tests} ({passed_tests/total_tests*100:.1f}%)")
        print(Fore.RED + f"Failed: {failed_tests} ({failed_tests/total_tests*100:.1f}%)")
        print(Fore.YELLOW + f"RAG Context Used: {rag_used}/{total_tests} tests ({rag_used/total_tests*100:.1f}%)")
        print(Fore.MAGENTA + f"Avg Response Time: {avg_response_time:.2f}s\n")
        
        # Detailed results
        print(Fore.CYAN + "Detailed Results:" + Fore.RESET)
        for result in self.test_results:
            status = "✓ PASS" if result['passed'] else "✗ FAIL"
            color = Fore.GREEN if result['passed'] else Fore.RED
            rag_status = "RAG" if result['rag_found'] else "NO-RAG"
            print(color + f"  Test {result['number']:2d}: {status} - {result['name']} [{rag_status}] ({result['response_time']:.2f}s)" + Fore.RESET)
        
        print()
        if passed_tests == total_tests:
            print(Fore.GREEN + "🎉 ALL TESTS PASSED! 🎉" + Fore.RESET)
        else:
            print(Fore.YELLOW + f"⚠ {failed_tests} test(s) need attention" + Fore.RESET)

def main():
    """Main test runner"""
    try:
        tester = OllamaRAGTester()
        tester.run_all_tests()
        tester.print_summary()
        
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n\nTest interrupted by user" + Fore.RESET)
    except Exception as e:
        print(Fore.RED + f"\n\nFatal error: {e}" + Fore.RESET)
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
