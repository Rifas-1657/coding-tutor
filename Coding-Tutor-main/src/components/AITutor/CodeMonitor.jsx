import { useEffect, useRef } from 'react';
import { monitorCode } from '../../services/api';

const CodeMonitor = ({ code, language, isActive, onObservationsUpdate }) => {
  const intervalRef = useRef(null);

  useEffect(() => {
    if (!isActive) {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
        intervalRef.current = null;
      }
      return;
    }

    // Monitor code every 3 seconds
    const monitor = async () => {
      if (!code || !code.trim()) return;

      try {
        const observations = await monitorCode(code, language);
        if (onObservationsUpdate) {
          onObservationsUpdate(observations);
        }
      } catch (error) {
        console.error('Code monitoring error:', error);
      }
    };

    // Initial monitor
    monitor();

    // Set up interval
    intervalRef.current = setInterval(monitor, 3000);

    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
    };
  }, [code, language, isActive, onObservationsUpdate]);

  return null; // This component doesn't render anything
};

export default CodeMonitor;

