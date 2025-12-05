# Quick Start Guide - Code Auditing Agent

This guide will help you get the Code Auditing Agent up and running in minutes.

## Prerequisites

- Python 3.8 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

## Installation Steps

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure API Key

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:

```
OPENAI_API_KEY=sk-your-actual-api-key-here
OPENAI_MODEL_NAME=gpt-4
```

### 3. Run the Agent

```bash
python code_auditing_agent.py
```

## What Happens Next?

The agent will:

1. **Read vulnerable_script.py** - Analyze the code for security issues
2. **Read config.yaml** - Check security configuration settings
3. **Identify vulnerabilities**:
   - Command Injection (os.system with user input)
   - SQL Injection (string concatenation in queries)
   - Cross-Site Scripting (unsanitized HTML output)
4. **Generate fixes** - Provide secure code alternatives
5. **Save suggestions** - Store recommendations in `security_suggestions/` folder

## Testing Without API Key

Run the test suite to verify the setup without requiring an API key:

```bash
python test_agent.py
```

This will:
- Test the custom tools (read_file_tool and suggest_fix_tool)
- Verify the vulnerable code contains expected security issues
- Check the configuration structure
- Confirm the agent components are properly set up

## Expected Output

When you run the agent with a valid API key, you'll see:

```
======================================================================
  Autonomous Code Auditing Agent - CrewAI Framework
======================================================================

✓ Language Model initialized successfully

Creating Security Auditor Agent...

✓ Agent created: Senior Python Security Auditor
✓ Task created: Security Audit of vulnerable_script.py

----------------------------------------------------------------------
Starting Code Audit Process...
----------------------------------------------------------------------

[Agent will analyze code, identify vulnerabilities, and suggest fixes]

======================================================================
  AUDIT COMPLETED
======================================================================

[Detailed security audit report appears here]

======================================================================
Check the 'security_suggestions' folder for detailed fix suggestions.
======================================================================
```

## Example Security Fix

The agent will generate fixes like this:

```python
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
```

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'crewai'"
**Solution**: Install dependencies: `pip install -r requirements.txt`

### Issue: "OPENAI_API_KEY not found"
**Solution**: Create `.env` file with your API key (see step 2 above)

### Issue: "Rate limit exceeded"
**Solution**: Wait a few minutes or upgrade your OpenAI plan

### Issue: Agent takes too long
**Solution**: 
- Use GPT-3.5-turbo instead of GPT-4 (faster but less accurate)
- Edit `.env`: `OPENAI_MODEL_NAME=gpt-3.5-turbo`

## Next Steps

1. **Customize the Agent**: Edit `code_auditing_agent.py` to:
   - Add more vulnerability patterns
   - Customize the agent's backstory
   - Add additional tools
   - Modify the audit task

2. **Add Your Own Code**: Replace `vulnerable_script.py` with your own code files

3. **Extend Functionality**: 
   - Add more custom tools
   - Create multiple agents for different types of audits
   - Integrate with CI/CD pipelines

## Learn More

- [CrewAI Documentation](https://docs.crewai.com/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Secure Coding Guidelines](https://owasp.org/www-project-secure-coding-practices-quick-reference-guide/)

## Support

If you encounter issues:
1. Check the [README.md](README.md) for detailed documentation
2. Review the test output: `python test_agent.py`
3. Verify your API key is valid and has credits
4. Check OpenAI service status

---

**Happy Auditing! 🔒**
