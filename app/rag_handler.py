"""
RAG Knowledge Base Handler
Tìm kiếm thông tin từ knowledge base để cung cấp context cho AI
"""
import json
import logging
from typing import Dict, List, Optional
from pathlib import Path

class RAGKnowledgeBase:
    def __init__(self, knowledge_path: str = "config/knowledge.json"):
        """
        Initialize RAG Knowledge Base
        
        Args:
            knowledge_path: Path to knowledge JSON file
        """
        self.knowledge_path = Path(knowledge_path)
        self.knowledge = self._load_knowledge()
        
        if not self.knowledge:
            logging.warning(f"Knowledge base empty or not found at {knowledge_path}")
        else:
            logging.info(f"✓ Loaded {len(self.knowledge)} knowledge entries")
    
    def _load_knowledge(self) -> Dict:
        """Load knowledge base from JSON file"""
        try:
            if not self.knowledge_path.exists():
                logging.warning(f"Knowledge file not found: {self.knowledge_path}")
                return {}
            
            with open(self.knowledge_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                logging.info(f"✓ Knowledge base loaded: {len(data)} entries")
                return data
        except Exception as e:
            logging.error(f"Error loading knowledge base: {e}")
            return {}
    
    def search(self, query: str, top_k: int = 3) -> List[Dict[str, any]]:
        """
        Search knowledge base for relevant information
        
        Args:
            query: User query
            top_k: Number of top results to return
            
        Returns:
            List of dicts with content and scores
        """
        if not self.knowledge:
            return []
        
        # Vietnamese stopwords - ignore these common words (but keep question words like 'ai', 'gì')
        stopwords = {'của', 'và', 'thì', 'với', 'cho', 'từ', 'này', 'đó', 
                     'như', 'được', 'các', 'để', 'trong', 'ở', 'về',
                     'hay', 'hoặc', 'nhưng', 'mà', 'thế', 'nào', 'đã', 'sẽ', 'bị'}
        
        query_lower = query.lower()
        query_words = set(query_lower.split()) - stopwords  # Remove stopwords
        results = []
        
        # Score each knowledge entry based on keyword matches
        scores = {}
        for key, entry in self.knowledge.items():
            keywords = entry.get('keywords', [])
            content = entry.get('content', '')
            
            score = 0
            matched_keywords = []
            
            for keyword in keywords:
                keyword_lower = keyword.lower()
                
                # Exact phrase match (highest priority) - bidirectional
                if keyword_lower in query_lower or query_lower in keyword_lower:
                    score += 10
                    matched_keywords.append(keyword)
                    continue
                
                # Word-level match (medium priority) - check if query words match keyword words
                keyword_words = set(keyword_lower.split())
                common_words = query_words & keyword_words
                if common_words:
                    score += 5 * len(common_words)
                    matched_keywords.append(keyword)
                    continue
                
                # Partial word match (low priority)
                for q_word in query_words:
                    if len(q_word) > 3:
                        for k_word in keyword_words:
                            if len(k_word) > 3:
                                if q_word[:3] in k_word or k_word[:3] in q_word:
                                    score += 2
                                    if keyword not in matched_keywords:
                                        matched_keywords.append(keyword)
                                    break
            
            if score > 0:
                scores[key] = {
                    'score': score,
                    'content': content,
                    'matched_keywords': matched_keywords,
                    'entry_key': key
                }
        
        # Sort by score and get top-k
        sorted_results = sorted(scores.items(), key=lambda x: x[1]['score'], reverse=True)
        
        for key, data in sorted_results[:top_k]:
            results.append(data)
            logging.info(f"[RAG] Match: {key} (score: {data['score']}, keywords: {data['matched_keywords']})")
        
        return results
    
    def get_context(self, query: str, max_length: int = 400, min_score: int = 10) -> Optional[str]:
        """
        Get combined context from search results
        
        Args:
            query: User query
            max_length: Maximum context length
            min_score: Minimum score required (default: 10, requires at least 1 exact match or 2 word matches)
            
        Returns:
            Combined context string or None
        """
        results = self.search(query, top_k=2)
        
        if not results:
            logging.info(f"[RAG] No context found for query: '{query}'")
            return None
        
        # Filter results by minimum score
        filtered_results = [r for r in results if r['score'] >= min_score]
        
        if not filtered_results:
            logging.info(f"[RAG] No context with sufficient score (min: {min_score}) for query: '{query}'")
            return None
        
        # Combine results with priority to highest scored
        context_parts = [result['content'] for result in filtered_results]
        context = " ".join(context_parts)
        
        logging.info(f"[RAG] Context matched: {len(filtered_results)} entries, total {len(context)} chars")
        
        # Trim if too long
        if len(context) > max_length:
            context = context[:max_length] + "..."
        
        return context
    
    def reload(self):
        """Reload knowledge base from file"""
        self.knowledge = self._load_knowledge()
        logging.info("Knowledge base reloaded")
