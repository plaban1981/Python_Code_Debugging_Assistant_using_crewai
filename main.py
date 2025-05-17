from crewai import Agent, Task, Crew, Process, LLM
from code_interpreter_tool import AnalyzeCodeTool, FixCodeTool, CodeInterpreterTool
import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv()

class correction(BaseModel):
    error: str = Field(..., description="List of original errors in the python code else None")
    fix: str = Field(..., description="Explanation of each fix applied for each error if any else None")
    rectifiled_code: str = Field(..., description="The corrected python code else the original code")

# Initialize the tools
analyze_tool = AnalyzeCodeTool()
fix_tool = FixCodeTool()
code_interpretor_tool = CodeInterpreterTool()

# Configure LLM with function calling
llm = LLM(
    #model="ollama/deepseek-r1:8b",
    model ='groq/llama-3.3-70b-versatile',
    temperature=0.0
)

# Create agents
manager_agent = Agent(
    role="Manager",
    goal="Oversee and coordinate the code analysis and correction process",
    backstory="I am an experienced software development manager who ensures code quality and coordinates between analysis and correction teams.",
    allow_delegation=True,
    verbose=True,
    llm=llm
)

analyzer_agent = Agent(
    role="Code Analyzer",
    goal="Identify syntax and logical errors in Python code",
    backstory="I am an expert at analyzing Python code and identifying potential issues and bugs.",
    tools=[analyze_tool, code_interpretor_tool],
    verbose=True,
    llm=llm
)

corrector_agent = Agent(
    role="Code Corrector",
    goal="Fix identified errors in Python code and output in the required JSON format",
    backstory="""I am specialized in fixing Python code issues while maintaining code quality and best practices.
    I always provide my output in valid JSON format matching the required schema.""",
    tools=[fix_tool, code_interpretor_tool],
    verbose=True,
    llm=llm
)

# Create tasks
analysis_task = Task(
    description="""
    Analyze the provided Python code and identify any syntax or logical errors.
    CODE:
    {code}
    List each error found with a clear explanation of what's wrong.
    """,
    expected_output="A detailed list of identified errors in the code, including syntax errors and logical issues with explanations",
    agent=analyzer_agent
)

correction_task = Task(
    description="""
    Your task is to analyze and fix Python code based on the analyzer agent's findings.
    You must return your response in valid JSON format exactly matching this structure:
    {
        "error": "<error description or 'None'>",
        "fix": "<fix explanation or 'None'>",
        "rectifiled_code": "<corrected code>"
    }
    
    Important:
    1. The output MUST be valid JSON
    2. All fields are required strings
    3. Use "None" (as a string) if no errors or fixes
    4. Ensure the rectifiled_code contains the complete code
    5. Do not include any additional text or formatting outside the JSON object
    """,
    expected_output="""A JSON object with three fields:
    - error: String describing the errors found or "None"
    - fix: String explaining the fixes applied or "None"
    - rectifiled_code: String containing the complete corrected code""",
    agent=corrector_agent,
    output_pydantic=correction,
    context=[analysis_task]
)

# Create the crew with hierarchical process
debugging_crew = Crew(
    agents=[analyzer_agent, corrector_agent],
    tasks=[analysis_task, correction_task],
    process=Process.hierarchical,
    manager_agent=manager_agent
)

# Function to run the debugging process
def debug_code(code: str):
    result = debugging_crew.kickoff(
        inputs={
            "code": code
        }
    )
    return result 