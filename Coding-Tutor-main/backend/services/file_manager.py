import os
from pathlib import Path
import re
from datetime import datetime

class FileManager:
    def __init__(self):
        self.storage_dir = Path(__file__).parent.parent / "storage" / "user_files"
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.max_file_size = 1024 * 1024  # 1MB limit
    
    def _sanitize_filename(self, filename):
        """Sanitize filename to prevent directory traversal attacks."""
        # Remove path separators and other dangerous characters
        filename = re.sub(r'[<>:"|?*\\/]', '_', filename)
        # Remove any .. patterns
        filename = filename.replace('..', '_')
        # Remove leading/trailing dots and spaces
        filename = filename.strip('. ')
        # Ensure it's not empty
        if not filename:
            filename = 'untitled'
        return filename
    
    def save_file(self, filename, content):
        """Save file to persistent storage."""
        # Check file size
        if len(content.encode('utf-8')) > self.max_file_size:
            raise ValueError(f"File size exceeds maximum of {self.max_file_size} bytes")
        
        filename = self._sanitize_filename(filename)
        file_path = self.storage_dir / filename
        
        # Write file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return str(file_path)
    
    def load_file(self, filename):
        """Load file from persistent storage."""
        filename = self._sanitize_filename(filename)
        file_path = self.storage_dir / filename
        
        if not file_path.exists():
            raise FileNotFoundError(f"File {filename} not found")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def list_files(self):
        """List all saved files with metadata."""
        files = []
        for file_path in self.storage_dir.iterdir():
            if file_path.is_file():
                stat = file_path.stat()
                files.append({
                    'filename': file_path.name,
                    'size': stat.st_size,
                    'modified': datetime.fromtimestamp(stat.st_mtime).isoformat()
                })
        
        # Sort by modified time, newest first
        files.sort(key=lambda x: x['modified'], reverse=True)
        return files
    
    def delete_file(self, filename):
        """Delete a file from persistent storage."""
        filename = self._sanitize_filename(filename)
        file_path = self.storage_dir / filename
        
        if not file_path.exists():
            raise FileNotFoundError(f"File {filename} not found")
        
        file_path.unlink()
        return True


