import React, { useState, useEffect, useCallback } from 'react';
import { getExercises } from '../../services/api';
import './LanguageSelector.css';

const ExerciseSelector = ({ language, exerciseId, onExerciseChange }) => {
  const [exercises, setExercises] = useState([]);
  const [loading, setLoading] = useState(false);

  const loadExercises = useCallback(async () => {
    if (!language) {
      setExercises([]);
      return;
    }
    
    setLoading(true);
    try {
      console.log('Loading exercises for language:', language);
      // Normalize language to lowercase
      const normalizedLang = language.toLowerCase();
      const data = await getExercises(normalizedLang);
      console.log('Exercises loaded:', data);
      if (Array.isArray(data) && data.length > 0) {
        setExercises(data);
      } else {
        console.warn('No exercises returned or empty array');
        setExercises([]);
      }
    } catch (error) {
      console.error('Error loading exercises:', error);
      console.error('Error details:', error.message, error.stack);
      setExercises([]);
      // Don't show alert - retry logic in API will handle backend startup timing
      // Only show error if backend is truly unavailable after all retries
      if (error.message.includes('after multiple retries')) {
        console.warn('Backend unavailable after retries');
      }
    } finally {
      setLoading(false);
    }
  }, [language]);

  useEffect(() => {
    loadExercises();
  }, [loadExercises]);

  const handleChange = (e) => {
    if (onExerciseChange) {
      onExerciseChange(e.target.value);
    }
  };

  return (
    <div className="language-selector">
      <label htmlFor="exercise-select">Exercise: </label>
      <select
        id="exercise-select"
        value={exerciseId || ''}
        onChange={handleChange}
        className="language-dropdown"
        disabled={loading || !language}
      >
        <option value="">
          {loading ? 'Loading exercises...' : exercises.length === 0 && language ? 'No exercises found' : 'Select an exercise...'}
        </option>
        {exercises.map((ex) => (
          <option key={ex.id} value={ex.id}>
            {ex.id}: {ex.title}
          </option>
        ))}
      </select>
      {!loading && language && exercises.length === 0 && (
        <span style={{ color: 'red', fontSize: '12px', marginLeft: '10px' }}>
          No exercises available. Check backend connection at http://localhost:8000
        </span>
      )}
    </div>
  );
};

export default ExerciseSelector;

