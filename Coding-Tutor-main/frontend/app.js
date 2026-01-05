// Lab Practice System - Frontend
const API_BASE = 'http://127.0.0.1:8000/api';

let currentLanguage = 'c';
let currentExerciseId = '';
let currentExercise = null;
let lastEvaluation = null;

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('language').addEventListener('change', handleLanguageChange);
    document.getElementById('exercise').addEventListener('change', handleExerciseChange);
    document.getElementById('run-btn').addEventListener('click', handleRun);
    document.getElementById('hint-btn').addEventListener('click', handleHint);
    
    loadExercises('c');
});

async function loadExercises(language) {
    try {
        const response = await fetch(`${API_BASE}/exercises/${language}`);
        const exercises = await response.json();
        
        const select = document.getElementById('exercise');
        select.innerHTML = '<option value="">Select an exercise...</option>';
        
        exercises.forEach(ex => {
            const option = document.createElement('option');
            option.value = ex.id;
            option.textContent = `${ex.id}: ${ex.title}`;
            select.appendChild(option);
        });
    } catch (error) {
        showOutput(`Error loading exercises: ${error.message}`, 'error');
    }
}

function handleLanguageChange(e) {
    currentLanguage = e.target.value;
    currentExerciseId = '';
    document.getElementById('exercise').value = '';
    loadExercises(currentLanguage);
}

function handleExerciseChange(e) {
    currentExerciseId = e.target.value;
}

async function handleRun() {
    const code = document.getElementById('code-editor').value.trim();
    
    if (!code) {
        showOutput('Please write some code first.', 'error');
        return;
    }
    
    if (!currentExerciseId) {
        showOutput('Please select an exercise first.', 'error');
        return;
    }
    
    showOutput('Running code...', 'info');
    document.getElementById('run-btn').disabled = true;
    
    try {
        const response = await fetch(`${API_BASE}/run`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                code: code,
                language: currentLanguage,
                exercise_id: currentExerciseId
            })
        });
        
        const result = await response.json();
        lastEvaluation = result;
        
        // Display results
        let output = `Execution Result: ${result.execution_result}\n`;
        output += `Test Summary: ${result.test_summary.passed}/${result.test_summary.total} passed\n\n`;
        output += `Decision: ${result.decision}\n`;
        output += `Message: ${result.message}\n`;
        output += `Learning Tip: ${result.learning_tip}\n\n`;
        
        // Show test results
        if (result.test_results) {
            output += 'Test Results:\n';
            output += '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n';
            result.test_results.forEach((tr, i) => {
                output += `\nTest Case ${i + 1}: ${tr.result}\n`;
                
                // Show test input (auto-provided)
                if (tr.test_input !== undefined && tr.test_input !== null && tr.test_input !== '') {
                    const inputDisplay = Array.isArray(tr.test_input) 
                        ? tr.test_input.join('\n') 
                        : String(tr.test_input);
                    output += `  Input (auto-provided): ${inputDisplay}\n`;
                }
                
                if (tr.passed) {
                    output += `  Output: ${tr.actual_output}\n`;
                    output += `  ✓ PASSED\n`;
                } else {
                    output += `  Expected: ${tr.expected_output}\n`;
                    output += `  Got: ${tr.actual_output}\n`;
                    output += `  ✗ FAILED\n`;
                }
                
                // Show warnings for this test
                if (tr.warnings && tr.warnings.length > 0) {
                    tr.warnings.forEach(warning => {
                        output += `  ⚠️ WARNING: ${warning}\n`;
                    });
                }
            });
            output += '\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n';
        }
        
        // Show global warnings
        if (result.warnings && result.warnings.length > 0) {
            output += '\n⚠️ LAB MODE WARNINGS:\n';
            result.warnings.forEach(warning => {
                output += `  • ${warning}\n`;
            });
        }
        
        showOutput(output, result.execution_result === 'PASS' ? 'success' : 'error');
        
        // Show hint button if hint is available
        if (result.hint_available) {
            document.getElementById('hint-btn').style.display = 'inline-block';
        } else {
            document.getElementById('hint-btn').style.display = 'none';
            document.getElementById('hint-section').style.display = 'none';
        }
        
    } catch (error) {
        showOutput(`Error: ${error.message}`, 'error');
    } finally {
        document.getElementById('run-btn').disabled = false;
    }
}

async function handleHint() {
    if (!lastEvaluation) {
        showOutput('Please run your code first.', 'error');
        return;
    }
    
    document.getElementById('hint-btn').disabled = true;
    document.getElementById('hint-content').textContent = 'Generating hint...';
    document.getElementById('hint-section').style.display = 'block';
    
    try {
        // Prepare error message and failed tests
        const failedTests = lastEvaluation.test_results
            .filter(tr => !tr.passed)
            .map(tr => `Test ${tr.testcase_index + 1}: Expected "${tr.expected_output}", Got "${tr.actual_output}"`)
            .join('\n');
        
        const errorMessage = lastEvaluation.error_type 
            ? `${lastEvaluation.error_type}: ${lastEvaluation.message}`
            : `Logical error: ${lastEvaluation.message}`;
        
        const response = await fetch(`${API_BASE}/hint`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                language: currentLanguage,
                exercise_id: currentExerciseId,
                error_message: errorMessage,
                failed_tests: failedTests
            })
        });
        
        const result = await response.json();
        document.getElementById('hint-content').textContent = result.hint;
        document.getElementById('hint-content').innerHTML += 
            `<br><small>Source: ${result.source}</small>`;
        
    } catch (error) {
        document.getElementById('hint-content').textContent = `Error: ${error.message}`;
    } finally {
        document.getElementById('hint-btn').disabled = false;
    }
}

function showOutput(text, type = 'info') {
    const output = document.getElementById('output');
    output.textContent = text;
    output.className = `output-box ${type}`;
}

