const API_BASE_URL = 'http://localhost:8000/api';

// Sandboxed Practice System API
export const runCode = async (code, language, exerciseId, userInput = '') => {
  try {
    const response = await fetch(`${API_BASE_URL}/run`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        code,
        language,
        exercise_id: exerciseId,
        user_input: userInput || '',
      }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error running code:', error);
    throw error;
  }
};

export const getExercises = async (language) => {
  try {
    // Normalize language to lowercase
    const normalizedLang = language.toLowerCase();
    const url = `${API_BASE_URL}/exercises/${normalizedLang}`;
    console.log('Fetching exercises from:', url);
    
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
      mode: 'cors',
    });

    console.log('Response status:', response.status);
    if (!response.ok) {
      const errorText = await response.text();
      console.error('Error response:', errorText);
      throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`);
    }

    const data = await response.json();
    console.log('Exercises data received:', data);
    console.log('Number of exercises:', Array.isArray(data) ? data.length : 'Not an array');
    return data;
  } catch (error) {
    console.error('Error getting exercises:', error);
    console.error('Error type:', error.constructor.name);
    console.error('Error message:', error.message);
    
    // Check if it's a network error
    if (error.message.includes('Failed to fetch') || error.message.includes('NetworkError') || error.name === 'TypeError') {
      const errorMsg = 'Cannot connect to backend server.\n\nPlease ensure:\n1. Backend is running: python backend/main.py\n2. Backend is on http://localhost:8000\n3. Check browser console for details';
      console.error('Network error:', errorMsg);
      throw new Error(errorMsg);
    }
    
    // Re-throw other errors
    throw error;
  }
};

export const getHint = async (language, exerciseId, errorMessage, failedTests) => {
  try {
    const response = await fetch(`${API_BASE_URL}/hint`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        language,
        exercise_id: exerciseId,
        error_message: errorMessage,
        failed_tests: failedTests,
      }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error getting hint:', error);
    throw error;
  }
};

export const monitorCode = async (code, language) => {
  try {
    const response = await fetch(`${API_BASE_URL}/ai-tutor/monitor`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        code,
        language,
      }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error monitoring code:', error);
    throw error;
  }
};

