"""
RAG and LLM Service for Lab Assistant
Integrates RAG retrieval from lab manuals and offline LLM for hints.
"""

import os
import sys
import subprocess
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any, Optional

# Configuration
EMBED_MODEL = "all-MiniLM-L6-v2"
OLLAMA_MODEL = "llama3.1"  # Change if using different model

# Paths - adjust based on project structure
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
INDEX_DIR = os.path.join(BASE_DIR, "indexes")
META_DIR = os.path.join(BASE_DIR, "metadata")

# Initialize embedder
try:
    embedder = SentenceTransformer(EMBED_MODEL)
except Exception as e:
    print(f"Warning: Could not load embedding model: {e}")
    embedder = None

# Cache for loaded indexes
indexes = {}
metadata = {}


class RAGLLMService:
    """Service for RAG retrieval and LLM hint generation."""
    
    def __init__(self):
        """Initialize RAG/LLM service."""
        self.embedder = embedder
        self.indexes = {}
        self.metadata = {}
    
    def load_subject(self, subject: str) -> bool:
        """
        Load FAISS index and metadata for a subject.
        
        Args:
            subject: Subject name (e.g., 'c_lab_manual', 'python_lab_manual')
        
        Returns:
            True if loaded successfully, False otherwise
        """
        if subject in self.indexes:
            return True
        
        try:
            index_path = os.path.join(INDEX_DIR, f"{subject}.index")
            meta_path = os.path.join(META_DIR, f"{subject}.npy")
            
            if not os.path.exists(index_path) or not os.path.exists(meta_path):
                return False
            
            self.indexes[subject] = faiss.read_index(index_path)
            self.metadata[subject] = np.load(meta_path, allow_pickle=True)
            return True
        except Exception as e:
            print(f"Error loading subject {subject}: {e}")
            return False
    
    def retrieve_notes(self, subject: str, query: str, k: int = 5) -> List[str]:
        """
        Retrieve relevant notes from lab manual using RAG.
        
        Args:
            subject: Subject name
            query: Search query
            k: Number of chunks to retrieve
        
        Returns:
            List of relevant text chunks
        """
        if not self.embedder:
            return []
        
        if not self.load_subject(subject):
            return []
        
        try:
            # Encode query
            q_vec = self.embedder.encode([query])
            
            # Search in FAISS index
            D, I = self.indexes[subject].search(q_vec, k)
            
            # Retrieve chunks
            chunks = [self.metadata[subject][i] for i in I[0]]
            return chunks
        except Exception as e:
            print(f"Error retrieving notes: {e}")
            return []
    
    def call_llm(self, prompt: str) -> str:
        """
        Call offline LLM (Ollama) for hint generation.
        
        Args:
            prompt: Prompt for LLM
        
        Returns:
            LLM response
        """
        try:
            # Check if ollama is available
            result = subprocess.run(
                ["ollama", "--version"],
                capture_output=True,
                text=True,
                timeout=2
            )
            if result.returncode != 0:
                return "LLM service (Ollama) is not available. Please install Ollama."
        except FileNotFoundError:
            return "LLM service (Ollama) is not installed. Please install Ollama to use AI hints."
        except Exception:
            pass
        
        try:
            process = subprocess.Popen(
                ["ollama", "run", OLLAMA_MODEL],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            output, error = process.communicate(prompt, timeout=30)
            
            if error:
                print(f"Ollama error: {error}")
            
            return output.strip() if output else "LLM response timeout or error."
        except subprocess.TimeoutExpired:
            process.kill()
            return "LLM response timeout. Please try again."
        except Exception as e:
            return f"LLM error: {str(e)}"
    
    def get_hint(
        self,
        subject: str,
        error_message: str,
        failed_tests: str,
        code: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate hint using RAG first, then LLM fallback.
        
        Args:
            subject: Subject name (e.g., 'c_lab_manual')
            error_message: Error message or description
            failed_tests: Description of failed test cases
            code: Optional student code (for context)
        
        Returns:
            dict with hint text and source
        """
        query = f"""
Error:
{error_message}

Failed Tests:
{failed_tests}
"""
        
        # 1. Try RAG first (lab notes)
        rag_chunks = self.retrieve_notes(subject, query, k=5)
        
        if rag_chunks and any(len(str(chunk)) > 50 for chunk in rag_chunks):
            # Format hint from RAG
            hint_text = self._format_hint_from_notes(rag_chunks, error_message, failed_tests)
            return {
                "hint": hint_text,
                "source": "RAG (Lab Manual)",
                "rag_used": True
            }
        
        # 2. Fallback to LLM
        hint_text = self._llm_hint_fallback(subject, error_message, failed_tests, code)
        return {
            "hint": hint_text,
            "source": "LLM (Ollama)",
            "rag_used": False
        }
    
    def _format_hint_from_notes(
        self,
        chunks: List[str],
        error_message: str,
        failed_tests: str
    ) -> str:
        """Format hint from RAG chunks using LLM."""
        notes = "\n\n".join(str(chunk) for chunk in chunks[:3])  # Use top 3 chunks
        
        prompt = f"""You are a lab assistant helping students learn programming.

IMPORTANT RULES:
- Do NOT provide full code
- Do NOT give complete solutions
- Give ONLY hints and guidance
- Point out where logic may be wrong
- Suggest what concept to revise
- Use simple, student-friendly language (Tanglish is okay)

LAB NOTES:
{notes}

ERROR CONTEXT:
{error_message}

FAILED TESTS:
{failed_tests}

Your task: Give a short, helpful hint (2-3 sentences) that guides the student to think and fix the code themselves.

Return ONLY the hint, nothing else."""

        return self.call_llm(prompt)
    
    def _llm_hint_fallback(
        self,
        subject: str,
        error_message: str,
        failed_tests: str,
        code: Optional[str] = None
    ) -> str:
        """Generate hint using LLM when RAG doesn't have relevant info."""
        prompt = f"""You are a strict programming lab assistant.

CRITICAL RULES:
- Do NOT write code
- Do NOT give full solution
- Give ONLY hints (2-3 sentences)
- Explain mistake conceptually
- Guide student to think, not copy

Context:
Subject: {subject}
Error: {error_message}
Failed Tests: {failed_tests}

Give clear, helpful hints that help the student understand the mistake and fix it themselves.
Use simple language (Tanglish is okay for explanations).

Return ONLY the hint."""

        return self.call_llm(prompt)


# Global instance
_rag_llm_service = None

def get_rag_llm_service() -> RAGLLMService:
    """Get or create global RAG/LLM service instance."""
    global _rag_llm_service
    if _rag_llm_service is None:
        _rag_llm_service = RAGLLMService()
    return _rag_llm_service

