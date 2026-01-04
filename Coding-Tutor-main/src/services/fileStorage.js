// File storage API service for persistent file operations

const API_BASE_URL = 'http://localhost:8000/api';

export const saveFileToStorage = async (filename, content) => {
  try {
    const response = await fetch(`${API_BASE_URL}/files/save`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        filename,
        content,
      }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || `HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error saving file:', error);
    throw error;
  }
};

export const loadFileFromStorage = async (filename) => {
  try {
    const response = await fetch(`${API_BASE_URL}/files/load/${encodeURIComponent(filename)}`);

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || `HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error loading file:', error);
    throw error;
  }
};

export const listFilesFromStorage = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/files/list`);

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return data.files || [];
  } catch (error) {
    console.error('Error listing files:', error);
    throw error;
  }
};

export const deleteFileFromStorage = async (filename) => {
  try {
    const response = await fetch(`${API_BASE_URL}/files/delete/${encodeURIComponent(filename)}`, {
      method: 'DELETE',
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || `HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error deleting file:', error);
    throw error;
  }
};


