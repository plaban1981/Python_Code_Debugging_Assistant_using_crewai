import subprocess
from typing import Dict, Any
from crewai.tools import BaseTool

class CodeInterpreterTool(BaseTool):
    name: str = "Code Interpreter"
    description: str = "Executes Python code and returns the result or error"

    def _run(self, code: str) -> Dict[str, Any]:
        try:
            result = subprocess.run(
                ['python', '-c', code],
                capture_output=True,
                text=True,
                timeout=10
            )
            return {
                "success": result.returncode == 0,
                "output": result.stdout,
                "error": result.stderr
            }
        except Exception as e:
            return {"error": str(e)}

class AnalyzeCodeTool(BaseTool):
    name: str = "Analyze Code"
    description: str = "Analyzes Python code for syntax and logical errors"

    def _run(self, code: str) -> str:
        interpreter = CodeInterpreterTool()
        result = interpreter._run(code)
        
        if result.get("error"):
            return f"Error found: {result['error']}"
        elif not result.get("success"):
            return f"Code execution failed: {result.get('error', 'Unknown error')}"
        else:
            return f"Code executed successfully. Output: {result.get('output', 'No output')}"

class FixCodeTool(BaseTool):
    name: str = "Fix Code"
    description: str = "Attempts to fix identified errors in Python code"

    def _run(self, code: str, errors: str) -> str:
        # First try to fix basic syntax errors
        fixed_code = self._fix_syntax(code)
        
        # Test if the fixes worked
        interpreter = CodeInterpreterTool()
        result = interpreter._run(fixed_code)
        
        if result.get("success"):
            return f"""
            Fixed code:
            {fixed_code}
            
            Execution result:
            {result.get('output', 'No output')}
            """
        else:
            return f"""
            Attempted fix (but errors remain):
            {fixed_code}
            
            Remaining errors:
            {result.get('error', 'Unknown error')}
            """

    def _fix_syntax(self, code: str) -> str:
        # Basic syntax fixes
        lines = code.split('\n')
        fixed_lines = []
        
        for line in lines:
            # Fix missing colons after function definitions
            if line.strip().startswith('def') and not line.strip().endswith(':'):
                line = line.rstrip() + ':'
            
            # Fix indentation
            if line.strip().startswith(('def', 'class', 'if', 'for', 'while')):
                next_line_should_indent = True
            elif line.strip() and not line.startswith(' '):
                line = '    ' + line
                
            fixed_lines.append(line)
            
        return '\n'.join(fixed_lines) 