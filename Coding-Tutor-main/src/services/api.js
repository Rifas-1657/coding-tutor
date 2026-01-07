const API_BASE_URL = 'http://localhost:8000/api';

// Retry configuration for backend startup timing
const MAX_RETRIES = 5;
const INITIAL_RETRY_DELAY = 500; // 500ms
const MAX_RETRY_DELAY = 5000; // 5 seconds

/**
 * Check if backend is ready by calling health endpoint
 */
async function checkBackendHealth() {
  try {
    const response = await fetch('http://localhost:8000/api/health', {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
      mode: 'cors',
    });
    return response.ok && response.status === 200;
  } catch (error) {
    return false;
  }
}

/**
 * Retry fetch with exponential backoff for handling backend startup timing
 * First checks backend health, then retries on connection failures
 */
async function fetchWithRetry(url, options = {}, retries = MAX_RETRIES, delay = INITIAL_RETRY_DELAY) {
  for (let attempt = 0; attempt <= retries; attempt++) {
    try {
      // On first attempt, check backend health first
      if (attempt === 0) {
        const isHealthy = await checkBackendHealth();
        if (!isHealthy && retries > 0) {
          console.log('Backend not ready, waiting for startup...');
          await new Promise(resolve => setTimeout(resolve, delay));
          delay = Math.min(delay * 2, MAX_RETRY_DELAY);
          continue;
        }
      }
      
      const response = await fetch(url, options);
      if (response.ok) {
        return response;
      }
      // If not the last attempt and it's a connection error, retry
      if (attempt < retries && (response.status === 0 || response.status >= 500)) {
        await new Promise(resolve => setTimeout(resolve, delay));
        delay = Math.min(delay * 2, MAX_RETRY_DELAY);
        continue;
      }
      return response;
    } catch (error) {
      // Network errors (ECONNREFUSED, Failed to fetch) - retry
      if (attempt < retries && (error.message.includes('Failed to fetch') || error.message.includes('ECONNREFUSED') || error.name === 'TypeError')) {
        console.log(`Backend connection failed, retrying in ${delay}ms... (attempt ${attempt + 1}/${retries + 1})`);
        await new Promise(resolve => setTimeout(resolve, delay));
        delay = Math.min(delay * 2, MAX_RETRY_DELAY);
        continue;
      }
      throw error;
    }
  }
}

// Sandboxed Practice System API
export const runCode = async (code, language, exerciseId, userInput = '') => {
  try {
    const response = await fetchWithRetry(`${API_BASE_URL}/run`, {
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
    
    const response = await fetchWithRetry(url, {
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
    
    // After all retries failed, provide helpful error message
    if (error.message.includes('Failed to fetch') || error.message.includes('NetworkError') || error.name === 'TypeError') {
      const errorMsg = 'Cannot connect to backend server after multiple retries.\n\nPlease ensure:\n1. Backend is running: python backend/main.py\n2. Backend is on http://localhost:8000\n3. Check browser console for details';
      console.error('Network error after retries:', errorMsg);
      throw new Error(errorMsg);
    }
    
    // Re-throw other errors
    throw error;
  }
};

export const getHint = async (language, exerciseId, errorMessage, failedTests) => {
  try {
    const response = await fetchWithRetry(`${API_BASE_URL}/hint`, {
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

