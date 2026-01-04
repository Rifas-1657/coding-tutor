import React, { useState, useEffect } from 'react';
import { saveFile, openFile } from '../../services/fileOperations';
import { saveFileToStorage, loadFileFromStorage, listFilesFromStorage } from '../../services/fileStorage';
import './FileControls.css';

const FileControls = ({ code, language, onFileLoaded }) => {
  const [recentFiles, setRecentFiles] = useState([]);
  const [showFileList, setShowFileList] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    loadFileList();
  }, []);

  const loadFileList = async () => {
    try {
      const files = await listFilesFromStorage();
      setRecentFiles(files);
    } catch (error) {
      console.error('Error loading file list:', error);
    }
  };

  const getDefaultExtension = () => {
    const extMap = {
      'c': '.c',
      'cpp': '.cpp',
      'python': '.py',
      'java': '.java',
    };
    return extMap[language] || '.c';
  };

  const getDefaultFilename = () => {
    return `untitled${getDefaultExtension()}`;
  };

  const handleNew = () => {
    if (code.trim() && window.confirm('Are you sure you want to create a new file? Unsaved changes will be lost.')) {
      window.location.reload();
    } else if (!code.trim()) {
      window.location.reload();
    }
  };

  const handleSave = async () => {
    setIsLoading(true);
    try {
      // First try to save via Electron/browser file dialog
      const defaultPath = getDefaultFilename();
      const result = await saveFile(code, defaultPath);
      
      if (result.success && result.path) {
        // Also save to persistent storage for quick access
        const filename = result.path.split(/[/\\]/).pop();
        try {
          await saveFileToStorage(filename, code);
          await loadFileList(); // Refresh file list
          alert(`File saved: ${filename}`);
        } catch (storageError) {
          // File dialog save succeeded, storage save failed - still OK
          console.warn('Could not save to persistent storage:', storageError);
        }
      } else if (!result.canceled) {
        alert(`Error saving file: ${result.error || 'Unknown error'}`);
      }
    } catch (error) {
      alert(`Error saving file: ${error.message}`);
    } finally {
      setIsLoading(false);
    }
  };

  const handleOpen = async () => {
    setIsLoading(true);
    try {
      const result = await openFile();
      
      if (result.success && result.content) {
        onFileLoaded(result);
        
        // Also save to persistent storage for recent files
        if (result.path) {
          const filename = result.path.split(/[/\\]/).pop();
          try {
            await saveFileToStorage(filename, result.content);
            await loadFileList();
          } catch (error) {
            // Ignore storage errors on open
            console.warn('Could not save to persistent storage:', error);
          }
        }
      } else if (!result.canceled && result.error) {
        alert(`Error opening file: ${result.error}`);
      }
    } catch (error) {
      alert(`Error opening file: ${error.message}`);
    } finally {
      setIsLoading(false);
    }
  };

  const handleLoadFromStorage = async (filename) => {
    setIsLoading(true);
    try {
      const result = await loadFileFromStorage(filename);
      if (result.success && result.content) {
        onFileLoaded({
          success: true,
          content: result.content,
          path: filename,
          extension: filename.split('.').pop().toLowerCase()
        });
        setShowFileList(false);
      }
    } catch (error) {
      alert(`Error loading file: ${error.message}`);
    } finally {
      setIsLoading(false);
    }
  };

  const formatFileSize = (bytes) => {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
  };

  const formatDate = (isoString) => {
    const date = new Date(isoString);
    return date.toLocaleString();
  };

  return (
    <div className="file-controls">
      <button className="file-button" onClick={handleNew} disabled={isLoading}>
        New
      </button>
      <button className="file-button" onClick={handleOpen} disabled={isLoading}>
        Open
      </button>
      <button className="file-button" onClick={handleSave} disabled={isLoading}>
        {isLoading ? 'Saving...' : 'Save'}
      </button>
      
      <div className="recent-files-container">
        <button
          className="file-button recent-files-button"
          onClick={() => setShowFileList(!showFileList)}
          disabled={isLoading}
        >
          Recent Files {showFileList ? '▲' : '▼'}
        </button>
        {showFileList && (
          <div className="recent-files-dropdown">
            {recentFiles.length === 0 ? (
              <div className="recent-files-empty">No saved files</div>
            ) : (
              recentFiles.map((file, index) => (
                <div
                  key={index}
                  className="recent-file-item"
                  onClick={() => handleLoadFromStorage(file.filename)}
                >
                  <div className="recent-file-name">{file.filename}</div>
                  <div className="recent-file-meta">
                    {formatFileSize(file.size)} • {formatDate(file.modified)}
                  </div>
                </div>
              ))
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default FileControls;
