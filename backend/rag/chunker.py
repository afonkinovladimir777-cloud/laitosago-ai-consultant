from typing import List, Dict
import re


class KnowledgeBaseProcessor:
    """Process knowledge base and extract documents with metadata"""
    
    def __init__(self, chunk_size: int = 400, overlap: int = 50):
        self.chunk_size = chunk_size
        self.overlap = overlap
    
    def load_knowledge_base(self, file_path: str) -> List[Dict]:
        """Load knowledge base from text file"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        documents = self.parse_documents(content)
        chunks = self.create_chunks(documents)
        
        return chunks
    
    def parse_documents(self, content: str) -> List[Dict]:
        """Parse documents from knowledge base content"""
        documents = []
        
        # Split by document markers
        doc_pattern = r'# DOC_ID: (\w+)\s*\n# CATEGORY: ([^\n]+)\s*\n# TITLE: ([^\n]+)\s*\n\n(.+?)(?=# DOC_ID:|$)'
        
        matches = re.finditer(doc_pattern, content, re.DOTALL)
        
        for match in matches:
            doc_id, category, title, text = match.groups()
            
            # Clean up text
            text = text.strip()
            
            documents.append({
                'doc_id': doc_id.strip(),
                'category': category.strip(),
                'title': title.strip(),
                'text': text,
                'full_text': text
            })
        
        return documents
    
    def create_chunks(self, documents: List[Dict]) -> List[Dict]:
        """Split documents into chunks with overlap"""
        chunks = []
        chunk_id = 0
        
        for doc in documents:
            text = doc['text']
            doc_chunks = self.split_into_chunks(text)
            
            for chunk_text in doc_chunks:
                chunk_id += 1
                chunks.append({
                    'chunk_id': chunk_id,
                    'doc_id': doc['doc_id'],
                    'category': doc['category'],
                    'title': doc['title'],
                    'text': chunk_text.strip(),
                    'metadata': {
                        'doc_id': doc['doc_id'],
                        'category': doc['category'],
                        'title': doc['title'],
                        'chunk_id': chunk_id
                    }
                })
        
        return chunks
    
    def split_into_chunks(self, text: str) -> List[str]:
        """Split text into chunks with overlap"""
        chunks = []
        
        # Split by sentences first
        sentences = re.split(r'(?<=[.!?])\s+', text)
        
        current_chunk = ""
        
        for sentence in sentences:
            if len(current_chunk) + len(sentence) < self.chunk_size:
                current_chunk += " " + sentence if current_chunk else sentence
            else:
                if current_chunk:
                    chunks.append(current_chunk)
                    # Add overlap
                    words = current_chunk.split()
                    overlap_text = " ".join(words[-max(len(words)//3, 5):])
                    current_chunk = overlap_text + " " + sentence
                else:
                    current_chunk = sentence
        
        if current_chunk:
            chunks.append(current_chunk)
        
        return chunks
