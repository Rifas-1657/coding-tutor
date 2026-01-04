import re
from typing import List, Dict, Optional

class AITutorService:
    def __init__(self):
        self.system_prompt = """You are a patient coding tutor helping students learn programming. Your role is to GUIDE students to discover solutions themselves, NOT to provide complete code.

CRITICAL RULES:
1. NEVER write complete working solutions
2. NEVER provide entire functions or full code blocks
3. NEVER give line-by-line code directly
4. ALWAYS ask leading questions
5. ALWAYS explain concepts, not just syntax
6. ALWAYS encourage experimentation
7. Point out logical issues without fixing them
8. If stuck, provide algorithm steps or pseudocode, NEVER actual code
9. Maximum code you can show: single syntax examples like `int x;` but never complete solutions

When students ask "how do I...", respond with:
- Concept explanations
- Questions that guide thinking
- Algorithm steps or pseudocode
- References to documentation
- Encouragement to try themselves

Be encouraging, patient, and focus on learning, not solving for them."""

    def analyze_code(self, code: str, language: str) -> Dict:
        """Analyze code structure and return observations."""
        observations = {
            "has_main_function": False,
            "variables_declared": [],
            "loops_present": [],
            "potential_issues": [],
            "code_length": len(code),
            "language": language
        }

        if not code or not code.strip():
            return observations

        # Check for main function (language-specific)
        if language.lower() in ['c', 'cpp']:
            observations["has_main_function"] = bool(re.search(r'\bmain\s*\(', code))
        elif language.lower() == 'python':
            observations["has_main_function"] = bool(re.search(r'\bdef\s+main\s*\(', code)) or '__main__' in code
        elif language.lower() == 'java':
            observations["has_main_function"] = bool(re.search(r'public\s+static\s+void\s+main', code))

        # Extract variables (simple heuristic)
        if language.lower() in ['c', 'cpp']:
            var_pattern = r'\b(int|float|double|char|bool)\s+(\w+)'
            observations["variables_declared"] = re.findall(var_pattern, code)
        elif language.lower() == 'python':
            # Python variable detection is harder, look for assignments
            var_pattern = r'^\s*(\w+)\s*='
            observations["variables_declared"] = re.findall(var_pattern, code, re.MULTILINE)

        # Detect loops
        loop_keywords = {
            'c': ['for', 'while', 'do'],
            'cpp': ['for', 'while', 'do'],
            'python': ['for', 'while'],
            'java': ['for', 'while', 'do']
        }
        for keyword in loop_keywords.get(language.lower(), []):
            if re.search(r'\b' + keyword + r'\s*\(', code):
                observations["loops_present"].append(keyword)

        # Potential issues (basic checks)
        if not observations["has_main_function"] and code.strip():
            observations["potential_issues"].append("No main function detected")
        
        if len(code) < 20:
            observations["potential_issues"].append("Very short code snippet")

        return observations

    async def get_tutor_response(
        self,
        message: str,
        current_code: str,
        language: str,
        conversation_history: List[Dict],
        code_observations: Optional[Dict] = None
    ) -> str:
        """Generate AI tutor response using code analysis and conversation context."""
        
        # Build context from code observations
        context_parts = []
        if code_observations:
            if code_observations.get("has_main_function"):
                context_parts.append("Student has a main function structure.")
            if code_observations.get("variables_declared"):
                context_parts.append(f"Student has declared some variables.")
            if code_observations.get("loops_present"):
                context_parts.append(f"Student is using: {', '.join(code_observations['loops_present'])} loops.")
            if code_observations.get("potential_issues"):
                context_parts.append(f"Issues noted: {', '.join(code_observations['potential_issues'])}")

        context = "\n".join(context_parts) if context_parts else "No specific code structure detected yet."

        # For now, use a simple rule-based response (can be replaced with LLM API call)
        # This is a placeholder - in production, call Claude/OpenAI/Local LLM
        
        # Simple pattern matching for common questions
        message_lower = message.lower()
        
        if any(word in message_lower for word in ['how do i', 'how to', 'how can i']):
            return self._generate_guiding_response(message, language, current_code)
        elif any(word in message_lower for word in ['write', 'code', 'show me', 'give me']):
            return ("I can't write the code for you, but I can guide you! What specific concept are you struggling with? "
                   "Let's break it down into steps. What have you tried so far?")
        else:
            return self._generate_guiding_response(message, language, current_code)

    def _generate_guiding_response(self, message: str, language: str, code: str) -> str:
        """Generate a guiding response based on the question."""
        # This is a simplified version - in production, use an actual LLM
        return (
            f"That's a great question! Let's think about this step by step.\n\n"
            f"For {language}, here's what you need to consider:\n"
            f"1. What data structures or variables do you need?\n"
            f"2. What operations are you trying to perform?\n"
            f"3. Have you thought about edge cases?\n\n"
            f"Try writing a small piece first and test it. What happens when you run what you have so far?"
        )

