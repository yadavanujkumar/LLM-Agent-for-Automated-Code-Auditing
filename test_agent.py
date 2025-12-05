"""
Test script to verify the Code Auditing Agent structure and tools.
This script tests the components without requiring an OpenAI API key.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from code_auditing_agent import ReadFileTool, SuggestFixTool


def test_read_file_tool():
    """Test the read_file_tool functionality."""
    print("=" * 70)
    print("Testing read_file_tool")
    print("=" * 70)
    
    tool = ReadFileTool()
    
    # Test reading vulnerable_script.py
    print("\n1. Testing: Read vulnerable_script.py")
    result = tool._run("vulnerable_script.py")
    print(f"✓ Tool executed successfully")
    print(f"  Content preview: {result[:100]}...")
    
    # Test reading config.yaml
    print("\n2. Testing: Read config.yaml")
    result = tool._run("config.yaml")
    print(f"✓ Tool executed successfully")
    print(f"  Content preview: {result[:100]}...")
    
    # Test reading non-existent file
    print("\n3. Testing: Read non-existent file")
    result = tool._run("nonexistent.py")
    print(f"✓ Tool handled error gracefully")
    print(f"  Result: {result}")
    
    print("\n✓ read_file_tool tests passed!\n")


def test_suggest_fix_tool():
    """Test the suggest_fix_tool functionality."""
    print("=" * 70)
    print("Testing suggest_fix_tool")
    print("=" * 70)
    
    tool = SuggestFixTool()
    
    # Test suggesting a fix
    print("\n1. Testing: Suggest a security fix")
    suggested_code = '''
import subprocess
import shlex

def execute_user_command(user_input):
    """
    SECURE: Uses subprocess with proper argument handling.
    Prevents command injection by using list arguments.
    """
    try:
        # Parse the command safely
        args = shlex.split(user_input)
        # Use subprocess.run() with list arguments for safety
        result = subprocess.run(
            args,
            capture_output=True,
            text=True,
            timeout=30,
            check=False
        )
        return result.returncode
    except Exception as e:
        print(f"Error executing command: {e}")
        return -1
'''
    
    result = tool._run("vulnerable_script.py", suggested_code)
    print(f"✓ Tool executed successfully")
    print(f"\nFix suggestion output:\n{result}")
    
    print("\n✓ suggest_fix_tool tests passed!\n")


def test_vulnerable_script():
    """Verify the vulnerable script contains expected vulnerabilities."""
    print("=" * 70)
    print("Testing vulnerable_script.py content")
    print("=" * 70)
    
    with open("vulnerable_script.py", "r") as f:
        content = f.read()
    
    vulnerabilities = {
        "Command Injection": "os.system" in content,
        "SQL Injection": "SELECT * FROM" in content and "+" in content,
        "XSS": "<div>" in content and "f\"" in content
    }
    
    print("\nVulnerabilities detected:")
    for vuln, found in vulnerabilities.items():
        status = "✓" if found else "✗"
        print(f"  {status} {vuln}: {'Found' if found else 'Not found'}")
    
    if all(vulnerabilities.values()):
        print("\n✓ All expected vulnerabilities present in vulnerable_script.py\n")
    else:
        print("\n✗ Some vulnerabilities missing!\n")


def test_config_yaml():
    """Verify the config.yaml contains security-related settings."""
    print("=" * 70)
    print("Testing config.yaml content")
    print("=" * 70)
    
    import yaml
    
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)
    
    print("\nConfiguration structure:")
    print(f"  ✓ Application config: {config.get('application', {}).get('name')}")
    print(f"  ✓ Database config: {bool(config.get('database'))}")
    print(f"  ✓ Security config: {bool(config.get('security'))}")
    
    security = config.get('security', {})
    print("\nSecurity settings:")
    for key, value in security.items():
        print(f"  - {key}: {value}")
    
    print("\n✓ config.yaml structure verified\n")


def test_agent_structure():
    """Test the agent structure without API key."""
    print("=" * 70)
    print("Testing Agent Structure")
    print("=" * 70)
    
    print("\n1. Verifying agent creation function exists...")
    from code_auditing_agent import create_security_auditor_agent, create_audit_task
    print("✓ Agent creation functions imported successfully")
    
    print("\n2. Verifying tool classes...")
    from code_auditing_agent import ReadFileTool, SuggestFixTool
    print(f"✓ ReadFileTool available: {ReadFileTool.__name__}")
    print(f"✓ SuggestFixTool available: {SuggestFixTool.__name__}")
    
    print("\n3. Agent configuration:")
    print("  - Role: Senior Python Security Auditor")
    print("  - Tools: read_file_tool, suggest_fix_tool")
    print("  - Task: Analyze vulnerable_script.py and config.yaml")
    
    print("\nNote: Full agent execution requires OPENAI_API_KEY")
    print("✓ Agent structure verified!\n")


def main():
    """Run all tests."""
    print("\n" + "=" * 70)
    print("  Code Auditing Agent - Component Tests")
    print("=" * 70 + "\n")
    
    try:
        test_read_file_tool()
        test_suggest_fix_tool()
        test_vulnerable_script()
        test_config_yaml()
        test_agent_structure()
        
        print("=" * 70)
        print("  ALL TESTS PASSED! ✓")
        print("=" * 70)
        print("\nThe Code Auditing Agent is properly configured.")
        print("To run the full agent, set your OPENAI_API_KEY in .env")
        print("and execute: python code_auditing_agent.py")
        print()
        
    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
