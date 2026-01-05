"""
Statistics Manager
Tracks only counts: total attempts, errors, hints used, language-wise counts.
NO code or input storage.
"""

from typing import Dict, Any
import json
import os


class StatsManager:
    """Manages statistics for lab practice system."""
    
    def __init__(self, stats_file: str = "stats.json"):
        """Initialize stats manager."""
        self.stats_file = stats_file
        self.stats = self._load_stats()
    
    def _load_stats(self) -> Dict[str, Any]:
        """Load statistics from file."""
        if os.path.exists(self.stats_file):
            try:
                with open(self.stats_file, 'r') as f:
                    return json.load(f)
            except Exception:
                pass
        
        # Default stats structure
        return {
            "total_attempts": 0,
            "total_errors": 0,
            "total_hints_used": 0,
            "language_counts": {
                "c": 0,
                "cpp": 0,
                "python": 0,
                "java": 0
            },
            "success_count": 0,
            "failure_count": 0
        }
    
    def _save_stats(self):
        """Save statistics to file."""
        try:
            with open(self.stats_file, 'w') as f:
                json.dump(self.stats, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save stats: {e}")
    
    def record_attempt(self, language: str, success: bool, error: bool = False, hint_used: bool = False):
        """
        Record an execution attempt.
        
        Args:
            language: Programming language
            success: Whether execution was successful
            error: Whether there was an error
            hint_used: Whether hint was requested
        """
        self.stats["total_attempts"] += 1
        
        if language in self.stats["language_counts"]:
            self.stats["language_counts"][language] += 1
        
        if success:
            self.stats["success_count"] += 1
        else:
            self.stats["failure_count"] += 1
        
        if error:
            self.stats["total_errors"] += 1
        
        if hint_used:
            self.stats["total_hints_used"] += 1
        
        self._save_stats()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get current statistics."""
        return self.stats.copy()

