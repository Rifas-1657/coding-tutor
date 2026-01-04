// WebSocket service for interactive terminal I/O

export class WebSocketExecutionService {
  constructor() {
    this.ws = null;
    this.onOutput = null;
    this.onError = null;
    this.onInputRequired = null;
    this.onComplete = null;
    this.reconnectAttempts = 0;
    this.maxReconnectAttempts = 3;
  }

  connect(onOutput, onError, onInputRequired, onComplete) {
    this.onOutput = onOutput;
    this.onError = onError;
    this.onInputRequired = onInputRequired;
    this.onComplete = onComplete;

    const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${wsProtocol}//${window.location.hostname}:8000/ws/execute`;
    
    this.ws = new WebSocket(wsUrl);

    this.ws.onopen = () => {
      console.log('WebSocket connected');
      this.reconnectAttempts = 0;
    };

    this.ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        
        switch (data.type) {
          case 'output':
            if (this.onOutput) this.onOutput(data.content);
            break;
          case 'error':
            if (this.onError) this.onError(data.content);
            break;
          case 'input_required':
            if (this.onInputRequired) this.onInputRequired(data.prompt || '');
            break;
          case 'complete':
            if (this.onComplete) this.onComplete(data);
            break;
          default:
            console.warn('Unknown message type:', data.type);
        }
      } catch (error) {
        console.error('Error parsing WebSocket message:', error);
      }
    };

    this.ws.onerror = (error) => {
      console.error('WebSocket error:', error);
      // Only show real errors from backend, not connection errors
    };

    this.ws.onclose = () => {
      console.log('WebSocket closed');
      // No auto-reconnect for batch execution - user can manually retry
    };
  }

  sendInput(input) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify({
        type: 'input',
        content: input
      }));
    }
  }

  executeCode(code, language, inputData = null, compileOnly = false) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      // Ensure input ends with newline if provided (for batch execution)
      let processedInput = inputData;
      if (processedInput && !processedInput.endsWith('\n')) {
        processedInput += '\n';
      }
      
      this.ws.send(JSON.stringify({
        type: 'execute',
        code,
        language,
        input_data: processedInput,
        compile_only: compileOnly
      }));
    } else {
      console.error('WebSocket not connected');
      if (this.onError) this.onError('Not connected to execution server');
    }
  }

  disconnect() {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
  }

  isConnected() {
    return this.ws && this.ws.readyState === WebSocket.OPEN;
  }
}

