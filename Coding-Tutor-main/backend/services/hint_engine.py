from typing import List
from models.hint_response import Hint, Severity

class HintEngine:
    def __init__(self):
        self.error_patterns = self._initialize_patterns()
    
    def _initialize_patterns(self) -> dict:
        """Initialize error patterns for each language."""
        return {
            'c': [
                {
                    'pattern': 'syntax error',
                    'severity': Severity.syntax,
                    'title': 'Syntax Error',
                    'description': 'There is a syntax error in your code. Check for missing semicolons, brackets, or parentheses.',
                    'example': 'Remember: C statements must end with a semicolon (;).'
                },
                {
                    'pattern': 'undefined reference',
                    'severity': Severity.runtime,
                    'title': 'Undefined Reference',
                    'description': 'A function or variable is being used but not defined. Check that all functions are declared or included.',
                    'example': None
                },
                {
                    'pattern': 'expected',
                    'severity': Severity.syntax,
                    'title': 'Expected Token',
                    'description': 'The compiler expected something different. Check the line number and compare with correct C syntax.',
                    'example': None
                },
                {
                    'pattern': 'assignment makes integer from pointer',
                    'severity': Severity.logic,
                    'title': 'Type Mismatch',
                    'description': 'You are trying to assign a pointer to an integer or vice versa. Review variable types and pointer usage.',
                    'example': None
                },
            ],
            'cpp': [
                {
                    'pattern': 'syntax error',
                    'severity': Severity.syntax,
                    'title': 'Syntax Error',
                    'description': 'There is a syntax error in your C++ code. Check for missing semicolons, brackets, or correct C++ syntax.',
                    'example': 'Remember: C++ statements must end with a semicolon (;).'
                },
                {
                    'pattern': 'no matching function',
                    'severity': Severity.logic,
                    'title': 'Function Not Found',
                    'description': 'The function you are calling does not match any available function signature. Check function name and parameters.',
                    'example': None
                },
                {
                    'pattern': 'was not declared',
                    'severity': Severity.syntax,
                    'title': 'Undeclared Identifier',
                    'description': 'A variable or function is being used before it is declared. Make sure to declare variables before use.',
                    'example': None
                },
            ],
            'python': [
                {
                    'pattern': 'SyntaxError',
                    'severity': Severity.syntax,
                    'title': 'Syntax Error',
                    'description': 'There is a syntax error in your Python code. Check indentation, colons, and proper Python syntax.',
                    'example': 'Remember: Python uses indentation (4 spaces) to define code blocks.'
                },
                {
                    'pattern': 'IndentationError',
                    'severity': Severity.syntax,
                    'title': 'Indentation Error',
                    'description': 'Python requires consistent indentation. Make sure all code blocks are indented with 4 spaces.',
                    'example': 'Use 4 spaces (not tabs) for indentation in Python.'
                },
                {
                    'pattern': 'NameError',
                    'severity': Severity.runtime,
                    'title': 'Name Error',
                    'description': 'A variable or function name is not defined. Check spelling and make sure variables are defined before use.',
                    'example': None
                },
                {
                    'pattern': 'TypeError',
                    'severity': Severity.logic,
                    'title': 'Type Error',
                    'description': 'You are performing an operation on incompatible types. Check the types of your variables.',
                    'example': 'Example: You cannot add a string and an integer without converting first.'
                },
                {
                    'pattern': 'IndexError',
                    'severity': Severity.runtime,
                    'title': 'Index Out of Range',
                    'description': 'You are trying to access an index that does not exist. Check the size of your list or array.',
                    'example': None
                },
                {
                    'pattern': 'ZeroDivisionError',
                    'severity': Severity.logic,
                    'title': 'Division by Zero',
                    'description': 'You are dividing by zero. Make sure the denominator is not zero before dividing.',
                    'example': None
                },
            ],
            'java': [
                {
                    'pattern': 'cannot find symbol',
                    'severity': Severity.syntax,
                    'title': 'Symbol Not Found',
                    'description': 'A variable, method, or class cannot be found. Check spelling and ensure proper imports.',
                    'example': None
                },
                {
                    'pattern': 'missing return statement',
                    'severity': Severity.syntax,
                    'title': 'Missing Return Statement',
                    'description': 'A method that should return a value does not have a return statement in all code paths.',
                    'example': None
                },
                {
                    'pattern': 'incompatible types',
                    'severity': Severity.logic,
                    'title': 'Type Incompatibility',
                    'description': 'You are trying to use incompatible types. Check variable types and method return types.',
                    'example': None
                },
                {
                    'pattern': 'ArrayIndexOutOfBoundsException',
                    'severity': Severity.runtime,
                    'title': 'Array Index Out of Bounds',
                    'description': 'You are accessing an array index that does not exist. Check array bounds before accessing elements.',
                    'example': None
                },
                {
                    'pattern': 'NullPointerException',
                    'severity': Severity.runtime,
                    'title': 'Null Pointer Exception',
                    'description': 'You are trying to use an object that is null. Make sure objects are initialized before use.',
                    'example': None
                },
            ]
        }
    
    def analyze_error(self, error_message: str, language: str) -> List[Hint]:
        """Analyze error message and generate hints."""
        if not error_message:
            return [Hint(
                severity=Severity.logic,
                title='No Error Message',
                description='Review your code carefully and check for common mistakes.',
                example=None
            )]
        
        error_lower = error_message.lower()
        language_lower = language.lower()
        
        hints = []
        patterns = self.error_patterns.get(language_lower, [])
        
        for pattern_info in patterns:
            if pattern_info['pattern'].lower() in error_lower:
                hints.append(Hint(
                    severity=pattern_info['severity'],
                    title=pattern_info['title'],
                    description=pattern_info['description'],
                    example=pattern_info.get('example')
                ))
        
        # If no specific pattern matches, provide generic hint
        if not hints:
            hints.append(Hint(
                severity=Severity.logic,
                title='Review Your Code',
                description='Read the error message carefully. Look at the line number mentioned and check for syntax or logic errors.',
                example='Pay attention to the error message details - they usually point to the exact problem.'
            ))
        
        return hints
    
    def analyze_code(self, code: str, language: str, error_message: str = None) -> List[Hint]:
        """Analyze code and error message to generate hints."""
        if error_message:
            return self.analyze_error(error_message, language)
        
        # Basic code analysis (could be expanded)
        if not code or len(code.strip()) == 0:
            return [Hint(
                severity=Severity.syntax,
                title='Empty Code',
                description='Please write some code before requesting hints.',
                example=None
            )]
        
        # Generic hint if no specific error
        return [Hint(
            severity=Severity.logic,
            title='Code Review',
            description='Review your code structure, logic flow, and check for common mistakes.',
            example=None
        )]

