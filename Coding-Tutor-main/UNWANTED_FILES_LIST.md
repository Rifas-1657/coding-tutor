# Unwanted Files in Coding-Tutor-main Folder

This document lists files that are **unwanted/unnecessary** and can be safely deleted.

## 🗑️ Files to Delete

### 1. **Empty Test/Example Files (Root Directory)**
These files are empty and serve no purpose:
- `student_code_example.py` ❌ (Empty file)
- `student_code_fixed.py` ❌ (Empty file)
- `test_fixed_code.py` ❌ (Empty file)
- `test_interactive_input.py` ❌ (Empty file)

### 2. **Duplicate Files (Root Directory)**
These are duplicates of files that exist in proper locations:
- `rag_llm_chat.py` ❌ (Empty, duplicate of `backend/rag/rag_llm_chat.py`)
- `build_index.py` ❌ (Duplicate of `backend/rag/build_index.py`)

### 3. **Unused Router Files**
These router files are NOT imported/used in `main.py`:
- `backend/routers/ai_tutor.py` ❌ (Not used - API uses `backend/api/` instead)
- `backend/routers/code_execution.py` ❌ (Not used)
- `backend/routers/files.py` ❌ (Not used)
- `backend/routers/hints.py` ❌ (Not used)
- `backend/routers/lab_exercises.py` ❌ (Not used)

**Note:** The actual API endpoints are in `backend/api/` folder which IS being used.

### 4. **Unused Service Files**
These service files might be duplicates or unused:
- `backend/services/rag_llm_service.py` ❌ (Duplicate functionality - `backend/rag/rag_llm_chat.py` is used instead)
- `backend/services/ai_tutor_service.py` ❌ (Not used - no imports found)
- `backend/services/compiler_manager.py` ❌ (Not used - Docker sandbox is used instead)
- `backend/services/file_manager.py` ❌ (Not used)
- `backend/services/hint_engine.py` ❌ (Not used - RAG module is used instead)
- `backend/services/interactive_execution.py` ❌ (Not used - sandbox_runner is used)
- `backend/services/lab_assistant.py` ❌ (Not used)
- `backend/services/sandbox.py` ❌ (Not used - sandbox_runner.py is used)
- `backend/services/websocket_execution.py` ❌ (Not used - REST API is used)

### 5. **Unused Sandbox Files**
- `backend/sandbox/input_injector.py` ❌ (Not used)
- `backend/sandbox/runner.py` ❌ (Not used - `services/sandbox_runner.py` is used instead)

### 6. **Old/Alternative Frontend**
The `frontend/` folder appears to be an old HTML/JS frontend, while the main app uses React in `src/`:
- `frontend/app.js` ❌ (Old frontend - React app in `src/` is the main one)
- `frontend/index.html` ❌ (Old frontend)
- `frontend/style.css` ❌ (Old frontend)

### 7. **Unused Evaluator**
- `backend/evaluator/test_runner.py` ❌ (Not used - test cases are handled in exercises JSON)

### 8. **Redundant Documentation Files**
Multiple documentation files that might overlap (keep only essential ones):
- `ARCHITECTURE_COMPLETE.md` ⚠️ (Might be redundant with README.md)
- `CODE_ANALYSIS_REPORT.md` ⚠️ (Analysis report - might be outdated)
- `DOCKER_SANDBOX_IMPLEMENTATION.md` ⚠️ (Implementation details - might be redundant)
- `FIXES_SUMMARY.md` ⚠️ (Temporary fix documentation)
- `INPUT_FIX_SUMMARY.md` ⚠️ (Temporary fix documentation)
- `INTEGRATION_COMPLETE.md` ⚠️ (Temporary integration docs)
- `INTEGRATION_GUIDE.md` ⚠️ (Might be redundant)
- `LAB_ASSISTANT_INTEGRATION.md` ⚠️ (Might be redundant)
- `PROJECT_SUMMARY.md` ⚠️ (Might be redundant with README.md)
- `REDESIGN_SUMMARY.md` ⚠️ (Temporary redesign docs)
- `SETUP.md` ⚠️ (Might be redundant with README.md and BACKEND_SETUP.md)

**Keep:**
- `README.md` ✅ (Main documentation)
- `BACKEND_SETUP.md` ✅ (Setup instructions - recently created)
- `requirements.txt` ✅ (Dependencies)

### 9. **Unused Offline Tutor Module**
The `offline_tutor/` folder appears to be a separate/old module:
- `offline_tutor/` folder ❌ (Entire folder - not used by main app)

### 10. **Test Files**
- `backend/test_sandbox.py` ⚠️ (Test file - keep if needed for testing, delete if not)

---

## 📊 Summary

### High Priority Deletions (Safe to Delete):
1. All empty test files in root
2. Duplicate files in root (`rag_llm_chat.py`, `build_index.py`)
3. Unused router files (`backend/routers/*`)
4. Unused service files (most of `backend/services/*` except `sandbox_runner.py`)
5. Unused sandbox files (`backend/sandbox/*`)
6. Old frontend folder (`frontend/`)
7. Offline tutor folder (`offline_tutor/`)

### Medium Priority (Review First):
- Redundant documentation files
- Test files (if not needed)

### Files to KEEP:
- `backend/api/` ✅ (Active API endpoints)
- `backend/services/sandbox_runner.py` ✅ (Used for code execution)
- `backend/rag/` ✅ (Used for hints)
- `backend/exercises/` ✅ (Exercise data)
- `backend/stats/` ✅ (Statistics)
- `src/` ✅ (React frontend)
- `backend/main.py` ✅ (Main server)
- `package.json`, `requirements.txt` ✅ (Dependencies)

---

## 🚀 Quick Cleanup Command

**Windows PowerShell:**
```powershell
# Delete empty test files
Remove-Item student_code_example.py, student_code_fixed.py, test_fixed_code.py, test_interactive_input.py

# Delete duplicate files
Remove-Item rag_llm_chat.py, build_index.py

# Delete unused routers
Remove-Item -Recurse backend\routers

# Delete unused services (keep sandbox_runner.py)
Remove-Item backend\services\rag_llm_service.py, backend\services\ai_tutor_service.py, backend\services\compiler_manager.py, backend\services\file_manager.py, backend\services\hint_engine.py, backend\services\interactive_execution.py, backend\services\lab_assistant.py, backend\services\sandbox.py, backend\services\websocket_execution.py

# Delete unused sandbox
Remove-Item -Recurse backend\sandbox

# Delete old frontend
Remove-Item -Recurse frontend

# Delete offline tutor
Remove-Item -Recurse offline_tutor

# Delete evaluator (if not needed)
Remove-Item -Recurse backend\evaluator
```

**Linux/Mac:**
```bash
# Delete empty test files
rm student_code_example.py student_code_fixed.py test_fixed_code.py test_interactive_input.py

# Delete duplicate files
rm rag_llm_chat.py build_index.py

# Delete unused folders
rm -rf backend/routers backend/sandbox frontend offline_tutor backend/evaluator

# Delete unused service files (keep sandbox_runner.py)
rm backend/services/rag_llm_service.py backend/services/ai_tutor_service.py backend/services/compiler_manager.py backend/services/file_manager.py backend/services/hint_engine.py backend/services/interactive_execution.py backend/services/lab_assistant.py backend/services/sandbox.py backend/services/websocket_execution.py
```

---

**Note:** Always backup your project before deleting files, or use version control (git) so you can restore if needed.
