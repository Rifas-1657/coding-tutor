# Lab Practice System

Offline Docker sandbox execution system for lab exercises with RAG/LLM hint generation.

## Architecture

```
lab-practice-system/
├── backend/
│   ├── sandbox/          # Docker execution
│   ├── rag/              # RAG/LLM hint generation
│   ├── exercises/        # Exercise JSON files (data-driven)
│   ├── evaluator/        # Test case evaluation
│   ├── stats/            # Statistics (counts only)
│   ├── api/              # REST API endpoints
│   └── main.py           # FastAPI application
├── frontend/             # Simple HTML/JS frontend
└── Lab/                  # Lab manual PDFs (for RAG indexing)
```

## Features

- ✅ **Docker Sandbox Execution** - Isolated, secure code execution
- ✅ **Non-Interactive Input** - Test cases injected upfront (no scanf/input() waiting)
- ✅ **Test Case Evaluation** - Automatic test case comparison
- ✅ **RAG/LLM Hints** - Conceptual hints from lab manuals or LLM
- ✅ **Data-Driven Exercises** - All exercises in JSON files (no hardcoding)
- ✅ **Statistics** - Tracks counts only (no code/input storage)

## Setup

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Build RAG Indexes:**
   ```bash
   cd backend/rag
   python build_index.py
   ```

3. **Start Backend:**
   ```bash
   cd backend
   python -m uvicorn main:app --reload
   ```

4. **Open Frontend:**
   Open `frontend/index.html` in a browser

## Usage Flow

1. Select Programming Language
2. Select Lab Exercise
3. Write Code
4. Click Run → Code executes in Docker with test cases
5. If tests fail → Hint button appears
6. Click Hint → Get conceptual hint (RAG-first, LLM-fallback)

## Future-Proof Design

- **Exercises**: All in JSON files - update without code changes
- **Lab Manuals**: PDFs in `Lab/` - rebuild indexes when updated
- **No Hardcoding**: System adapts to new exercises automatically

## Important Notes

- **No File Storage**: Code execution is temporary, no files saved
- **Non-Interactive**: All input comes from test cases (no keyboard input)
- **Offline**: Works completely offline (Docker + Ollama LLM)
