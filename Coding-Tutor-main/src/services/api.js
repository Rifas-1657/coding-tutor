const API_BASE_URL = 'http://localhost:8000/api';

export const runCode = async (code, language, inputData = null) => {
  try {
    const response = await fetch(`${API_BASE_URL}/run-code`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        code,
        language,
        input_data: inputData || null,
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

export const getHint = async (code, language, errorMessage = null) => {
  try {
    const response = await fetch(`${API_BASE_URL}/get-hint`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        code,
        language,
        error_message: errorMessage,
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

