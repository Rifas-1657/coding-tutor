"""
RAG and LLM Service for Hint Generation
RAG-first, LLM-fallback strategy for generating conceptual hints.
"""

import os
import faiss
import numpy as np
import subprocess
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any, Optional

# Configuration
EMBED_MODEL = "all-MiniLM-L6-v2"
OLLAMA_MODEL = "llama3.1"

# Paths
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

# Cache for RAG retrieval results (per exercise)
_rag_cache = {}


def load_subject(subject: str) -> bool:
    """Load FAISS index and metadata for a subject."""
    if subject in indexes:
        return True
    
    try:
        index_path = os.path.join(INDEX_DIR, f"{subject}.index")
        meta_path = os.path.join(META_DIR, f"{subject}.npy")
        
        if not os.path.exists(index_path) or not os.path.exists(meta_path):
            return False
        
        indexes[subject] = faiss.read_index(index_path)
        metadata[subject] = np.load(meta_path, allow_pickle=True)
        return True
    except Exception as e:
        print(f"Error loading subject {subject}: {e}")
        return False


def retrieve_notes(subject: str, query: str, k: int = 5) -> List[str]:
    """Retrieve relevant notes from lab manual using RAG with caching."""
    if not embedder:
        return []
    
    if not load_subject(subject):
        return []
    
    # Check cache first
    cache_key = f"{subject}:{hash(query)}"
    if cache_key in _rag_cache:
        return _rag_cache[cache_key]
    
    try:
        q_vec = embedder.encode([query])
        D, I = indexes[subject].search(q_vec, k)
        result = [metadata[subject][i] for i in I[0]]
        
        # Cache result (limit cache size to prevent memory issues)
        if len(_rag_cache) < 100:  # Keep max 100 cached queries
            _rag_cache[cache_key] = result
        
        return result
    except Exception as e:
        print(f"Error retrieving notes: {e}")
        return []


def call_llm(prompt: str) -> str:
    """Call offline LLM (Ollama) for hint generation."""
    try:
        # Check if ollama is available
        result = subprocess.run(
            ["ollama", "--version"],
            capture_output=True,
            text=True,
            timeout=2,
            encoding='utf-8',
            errors='replace'
        )
        if result.returncode != 0:
            return "LLM service (Ollama) is not available."
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
            text=True,
            encoding='utf-8',
            errors='replace'
        )
        output, error = process.communicate(prompt, timeout=30)
        
        if error:
            print(f"Ollama error: {error}")
        
        return output.strip() if output else "LLM response timeout or error."
    except subprocess.TimeoutExpired:
        if 'process' in locals():
            process.kill()
        return "LLM response timeout. Please try again."
    except Exception as e:
        return f"LLM error: {str(e)}"


def format_hint_from_notes(chunks: List[str], error_message: str, failed_tests: str) -> str:
    """Format hint from RAG chunks using LLM."""
    notes = "\n\n".join(str(chunk) for chunk in chunks[:3])
    
    prompt = f"""You are a lab assistant helping students learn programming.

CRITICAL RULES:
- Do NOT provide full code or complete solutions
- Give ONLY hints and guidance (2-3 sentences)
- Point out where logic may be wrong
- Suggest what concept to revise
- Use simple language - you can use Tanglish, Hindi, or English as needed
- Help student think, don't give answers

LAB NOTES:
{notes}

ERROR CONTEXT:
{error_message}

FAILED TESTS:
{failed_tests}

Your task: Give a short, helpful hint that guides the student to think and fix the code themselves.
You can explain in Tanglish, Hindi, or English - whatever helps the student understand better.

Return ONLY the hint, nothing else."""

    return call_llm(prompt)


def llm_hint_fallback(subject: str, error_message: str, failed_tests: str) -> str:
    """Generate hint using LLM when RAG doesn't have relevant info."""
    prompt = f"""You are a strict programming lab assistant.

CRITICAL RULES:
- Do NOT write code or give full solutions
- Give ONLY hints (2-3 sentences)
- Explain mistake conceptually
- Guide student to think, not copy
- Use simple language - Tanglish, Hindi, or English as needed

Context:
Subject: {subject}
Error: {error_message}
Failed Tests: {failed_tests}

Give clear, helpful hints that help the student understand the mistake and fix it themselves.
You can explain in Tanglish, Hindi, or English - whatever helps the student understand better.

Return ONLY the hint, nothing else."""

    return call_llm(prompt)


def generate_rule_based_hint(error_message: str, failed_tests: str) -> Optional[str]:
    """
    Generate fast rule-based hints for common errors.
    Returns hint string if rule matches, None otherwise.
    """
    error_lower = error_message.lower()
    tests_lower = failed_tests.lower()
    
    # Rule 1: Output format error (prompt text detected)
    if "output_format_error" in error_lower or "prompt" in error_lower:
        return "Your program is printing input prompts. In lab practice, print ONLY the final result, not prompts like 'Enter a number:' or 'Input:'. Remove all printf/print statements that ask for input."
    
    # Rule 2: Compilation error
    if "compile" in error_lower or "syntax" in error_lower:
        if "missing" in error_lower or "expected" in error_lower:
            return "Syntax error: Missing semicolons, brackets, or parentheses. Error message la exact line number check pannunga. (Check the exact line number in the error message.)"
        return "Compilation error: Code syntax check pannunga. All statements properly close pannirukka verify pannunga. (Check your code syntax and ensure all statements are properly closed.)"
    
    # Rule 3: Runtime error
    if "runtime" in error_lower or "segmentation" in error_lower or "null pointer" in error_lower:
        return "Runtime error: Array bounds, null pointer, or division by zero check pannunga. Variables initialize pannirukka verify pannunga. (Check array bounds, null pointer access, or division by zero. Verify all variables are initialized.)"
    
    # Rule 4: Output mismatch - numeric
    if "output mismatch" in error_lower or "expected" in error_lower:
        if any(char.isdigit() for char in failed_tests):
            return "Output match aagala. Calculation logic check pannunga. Formula correct-a use pannirukkingala? Decimal places handle pannirukkingala? (Your output doesn't match. Check calculation logic and formula.)"
        return "Output format mismatch. Spacing, newlines, decimal places exact-a match pannunga. (Ensure output format matches exactly.)"
    
    # Rule 5: Logical error
    if "logical" in error_lower:
        return "Logical error: Algorithm review pannunga. Loop conditions correct-a? Variables right order-la update pannirukkingala? Step by step trace pannunga. (Review algorithm and loop conditions.)"
    
    # Rule 6: Missing output
    if "no output" in error_lower or "empty" in error_lower:
        return "Output print aagala. printf/print/cout use pannirukkingala? Code print statement reach aagudha check pannunga. (No output. Check if you're using printf/print/cout and if code reaches print statement.)"
    
    return None


def get_hint(subject: str, error_message: str, failed_tests: str) -> Dict[str, Any]:
    """
    Generate hint using rule-based first, then RAG, then LLM fallback.
    
    Args:
        subject: Subject name (e.g., 'c_lab_manual', 'python_lab_manual')
        error_message: Error description
        failed_tests: Description of failed test cases
    
    Returns:
        dict with hint, source, and rag_used flag
    """
    # Step 1: Try rule-based hints first (FAST, <1s)
    rule_hint = generate_rule_based_hint(error_message, failed_tests)
    if rule_hint:
        return {
            "hint": rule_hint,
            "source": "Rule-based (Fast)",
            "rag_used": False
        }
    
    # Step 2: Try RAG (lab notes) for conceptual hints
    query = f"""
Error:
{error_message}

Failed Tests:
{failed_tests}
"""
    
    rag_chunks = retrieve_notes(subject, query, k=5)
    
    if rag_chunks and any(len(str(chunk)) > 50 for chunk in rag_chunks):
        hint_text = format_hint_from_notes(rag_chunks, error_message, failed_tests)
        return {
            "hint": hint_text,
            "source": "RAG (Lab Manual)",
            "rag_used": True
        }
    
    # Step 3: Fallback to LLM (slowest, use only when needed)
    hint_text = llm_hint_fallback(subject, error_message, failed_tests)
    return {
        "hint": hint_text,
        "source": "LLM (Ollama)",
        "rag_used": False
    }

