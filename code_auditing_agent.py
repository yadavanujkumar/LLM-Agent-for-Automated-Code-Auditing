"""
Autonomous Code Auditing Agent using CrewAI Framework
This script implements a security auditing agent that analyzes code for vulnerabilities.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from crewai.tools import BaseTool
from langchain_openai import ChatOpenAI
from typing import Type
from pydantic import BaseModel, Field
import json


# Load environment variables
load_dotenv()


class ReadFileInput(BaseModel):
    """Input schema for read_file_tool."""
    path: str = Field(..., description="The file path to read")


class SuggestFixInput(BaseModel):
    """Input schema for suggest_fix_tool."""
    path: str = Field(..., description="The file path where the fix should be applied")
    suggested_code: str = Field(..., description="The suggested fixed code block")


class ReadFileTool(BaseTool):
    """
    Custom tool to read the contents of a specified file.
    This allows the agent to examine code files for security issues.
    """
    name: str = "read_file_tool"
    description: str = (
        "Reads and returns the complete contents of a specified file. "
        "Use this tool to examine source code files for security vulnerabilities. "
        "Input should be a valid file path relative to the project root."
    )
    args_schema: Type[BaseModel] = ReadFileInput

    def _run(self, path: str) -> str:
        """Execute the tool to read a file."""
        try:
            # Get the base directory (project root)
            base_dir = Path(__file__).parent
            file_path = base_dir / path
            
            # Check if file exists
            if not file_path.exists():
                return f"Error: File '{path}' not found."
            
            # Read and return file contents
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            return f"File: {path}\n\n{content}"
        
        except Exception as e:
            return f"Error reading file '{path}': {str(e)}"


class SuggestFixTool(BaseTool):
    """
    Custom tool to output suggested fixes in a structured format.
    This allows the agent to document its security recommendations.
    """
    name: str = "suggest_fix_tool"
    description: str = (
        "Outputs a suggested code fix in a structured format. "
        "Use this tool to document your security recommendations and provide "
        "safe, refactored code that addresses the identified vulnerabilities. "
        "This simulates a commit suggestion or pull request comment."
    )
    args_schema: Type[BaseModel] = SuggestFixInput

    def _run(self, path: str, suggested_code: str) -> str:
        """Execute the tool to suggest a fix."""
        try:
            # Create a structured output
            fix_suggestion = {
                "file": path,
                "status": "SECURITY_FIX_SUGGESTED",
                "suggested_code": suggested_code,
                "timestamp": "2024-01-01T00:00:00Z"  # Simulated timestamp
            }
            
            # Format the output nicely
            output = f"""
=== SECURITY FIX SUGGESTION ===
File: {path}
Status: {fix_suggestion['status']}

Suggested Code:
{'-' * 50}
{suggested_code}
{'-' * 50}

This fix has been documented and is ready for review.
"""
            
            # Also save to a file for persistence
            base_dir = Path(__file__).parent
            suggestions_dir = base_dir / "security_suggestions"
            suggestions_dir.mkdir(exist_ok=True)
            
            suggestion_file = suggestions_dir / f"{Path(path).stem}_fix.txt"
            with open(suggestion_file, 'w', encoding='utf-8') as f:
                f.write(output)
            
            return output + f"\n✓ Fix suggestion saved to: {suggestion_file}"
        
        except Exception as e:
            return f"Error suggesting fix for '{path}': {str(e)}"


def create_security_auditor_agent(llm):
    """
    Create the Senior Python Security Auditor agent.
    
    Args:
        llm: The language model to use for the agent
    
    Returns:
        Agent: The configured security auditor agent
    """
    # Initialize custom tools
    read_file_tool = ReadFileTool()
    suggest_fix_tool = SuggestFixTool()
    
    # Define the agent
    agent = Agent(
        role="Senior Python Security Auditor",
        goal=(
            "Meticulously analyze Python code for security vulnerabilities, "
            "identify OWASP Top 10 issues (SQL Injection, XSS, Command Injection, etc.), "
            "and provide industry-standard, secure code fixes."
        ),
        backstory=(
            "You are a highly experienced security professional with over 15 years "
            "of expertise in application security. You meticulously review code for "
            "OWASP Top 10 vulnerabilities including SQL Injection (SQLi), "
            "Cross-Site Scripting (XSS), Command Injection, and other security flaws. "
            "You have a deep understanding of secure coding practices and always "
            "suggest industry-standard fixes that follow security best practices. "
            "Your recommendations are precise, actionable, and help developers "
            "write more secure code."
        ),
        tools=[read_file_tool, suggest_fix_tool],
        llm=llm,
        verbose=True,
        allow_delegation=False
    )
    
    return agent


def create_audit_task(agent):
    """
    Create the code auditing task.
    
    Args:
        agent: The agent that will perform the task
    
    Returns:
        Task: The configured auditing task
    """
    task = Task(
        description=(
            "Perform a comprehensive security audit with the following steps:\n\n"
            "1. Use the read_file_tool to analyze 'vulnerable_script.py' and identify "
            "all security vulnerabilities present in the code. Look specifically for:\n"
            "   - Command Injection vulnerabilities (unsafe command execution)\n"
            "   - SQL Injection vulnerabilities (unsafe query construction)\n"
            "   - Cross-Site Scripting (XSS) vulnerabilities (unsafe content rendering)\n"
            "   - Any other OWASP Top 10 security issues\n\n"
            "2. Use the read_file_tool to check 'config.yaml' for related security "
            "configuration variables that may impact the vulnerabilities.\n\n"
            "3. For each identified vulnerability, provide:\n"
            "   - A clear description of the security risk\n"
            "   - The potential impact if exploited\n"
            "   - OWASP category classification\n\n"
            "4. Use the suggest_fix_tool to provide a precise, safe refactored code "
            "block for the most critical vulnerability. The fix should:\n"
            "   - Follow security best practices\n"
            "   - Use safe alternatives (e.g., subprocess.run() with list arguments)\n"
            "   - Include proper input validation\n"
            "   - Add security comments explaining the fix\n\n"
            "Be thorough, precise, and ensure your recommendations follow "
            "industry-standard secure coding practices."
        ),
        expected_output=(
            "A comprehensive security audit report that includes:\n"
            "1. List of all identified vulnerabilities with descriptions\n"
            "2. OWASP classifications for each vulnerability\n"
            "3. Assessment of configuration file security settings\n"
            "4. A detailed, safe refactored code block for the critical vulnerability\n"
            "5. Recommendations for secure coding practices"
        ),
        agent=agent
    )
    
    return task


def main():
    """
    Main execution function for the Code Auditing Agent.
    """
    print("=" * 70)
    print("  Autonomous Code Auditing Agent - CrewAI Framework")
    print("=" * 70)
    print()
    
    # Check for OpenAI API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == "your_openai_api_key_here":
        print("⚠️  WARNING: OPENAI_API_KEY not found or not set!")
        print("Please create a .env file with your OpenAI API key.")
        print("You can use .env.example as a template.")
        print()
        print("For demonstration purposes, the agent structure will be created,")
        print("but you'll need a valid API key to run the actual audit.")
        print()
        # For demonstration, we'll continue with a placeholder
        # In production, you would return here
    
    # Initialize the LLM
    try:
        llm = ChatOpenAI(
            model=os.getenv("OPENAI_MODEL_NAME", "gpt-4"),
            temperature=0.1  # Low temperature for more consistent security analysis
        )
        print("✓ Language Model initialized successfully")
    except Exception as e:
        print(f"✗ Error initializing LLM: {e}")
        print("Please ensure your OPENAI_API_KEY is set correctly in .env file")
        return
    
    print()
    print("Creating Security Auditor Agent...")
    print()
    
    # Create the agent
    auditor_agent = create_security_auditor_agent(llm)
    print("✓ Agent created: Senior Python Security Auditor")
    
    # Create the task
    audit_task = create_audit_task(auditor_agent)
    print("✓ Task created: Security Audit of vulnerable_script.py")
    
    print()
    print("-" * 70)
    print("Starting Code Audit Process...")
    print("-" * 70)
    print()
    
    # Create and run the crew
    crew = Crew(
        agents=[auditor_agent],
        tasks=[audit_task],
        process=Process.sequential,
        verbose=True
    )
    
    try:
        # Execute the audit
        result = crew.kickoff()
        
        print()
        print("=" * 70)
        print("  AUDIT COMPLETED")
        print("=" * 70)
        print()
        print(result)
        print()
        print("=" * 70)
        print("Check the 'security_suggestions' folder for detailed fix suggestions.")
        print("=" * 70)
        
    except Exception as e:
        print()
        print("=" * 70)
        print("  ERROR DURING AUDIT")
        print("=" * 70)
        print(f"An error occurred: {e}")
        print()
        print("Common issues:")
        print("1. Missing or invalid OPENAI_API_KEY in .env file")
        print("2. Network connectivity issues")
        print("3. API rate limits or quota exceeded")
        print()
        print("Please check your configuration and try again.")


if __name__ == "__main__":
    main()
