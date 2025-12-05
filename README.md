# LLM-Agent-for-Automated-Code-Auditing

An autonomous Code Auditing Agent built with the CrewAI framework that analyzes code for security vulnerabilities and suggests fixes using AI-powered reasoning and custom tools.

## 🎯 Overview

This project demonstrates a practical implementation of an agentic AI system for automated security code auditing. The agent:

- **Analyzes** Python code files for security vulnerabilities
- **Identifies** OWASP Top 10 security issues (SQL Injection, XSS, Command Injection, etc.)
- **Suggests** industry-standard fixes with detailed explanations
- **Uses custom tools** to read files and document security recommendations

## 🏗️ Architecture

### Agent Persona: Senior Python Security Auditor
- **Role**: Expert security professional with 15+ years of experience
- **Goal**: Identify and fix OWASP Top 10 vulnerabilities
- **Capabilities**: Uses custom tools to read code and suggest fixes

### Custom Tools

1. **read_file_tool(path)**: Reads and analyzes file contents
2. **suggest_fix_tool(path, suggested_code)**: Outputs structured fix suggestions

### Simulated Repository Files

- **vulnerable_script.py**: Contains intentional security vulnerabilities:
  - Command Injection (unsafe os.system() usage)
  - SQL Injection (string concatenation in queries)
  - Cross-Site Scripting (XSS) (unsanitized user content)

- **config.yaml**: Application configuration with security settings

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- OpenAI API key (for GPT-4 or GPT-3.5)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yadavanujkumar/LLM-Agent-for-Automated-Code-Auditing.git
   cd LLM-Agent-for-Automated-Code-Auditing
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure API key**:
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key
   ```

### Usage

Run the code auditing agent:

```bash
python code_auditing_agent.py
```

The agent will:
1. Read and analyze `vulnerable_script.py`
2. Check `config.yaml` for security-related configurations
3. Identify all vulnerabilities with OWASP classifications
4. Generate detailed fix suggestions
5. Save recommendations to the `security_suggestions/` folder

## 📋 Example Output

The agent produces a comprehensive security audit report including:

- **Vulnerability Identification**: Lists all security issues found
- **OWASP Classification**: Categorizes each vulnerability
- **Impact Assessment**: Explains potential security risks
- **Code Fixes**: Provides safe, refactored code blocks
- **Best Practices**: Recommends secure coding standards

Example fix suggestion structure:
```
=== SECURITY FIX SUGGESTION ===
File: vulnerable_script.py
Status: SECURITY_FIX_SUGGESTED

Suggested Code:
--------------------------------------------------
import subprocess
import shlex

def execute_user_command(user_input):
    """
    SECURE: Uses subprocess with proper argument handling
    """
    # Use subprocess.run() with list arguments for safety
    try:
        # Parse the command safely
        args = shlex.split(user_input)
        result = subprocess.run(args, capture_output=True, text=True, timeout=30)
        return result.returncode
    except Exception as e:
        print(f"Error executing command: {e}")
        return -1
--------------------------------------------------
```

## 🛠️ Technical Stack

- **CrewAI**: Agent orchestration framework
- **LangChain-OpenAI**: LLM integration
- **Python-dotenv**: Environment variable management
- **PyYAML**: Configuration file parsing

## 📁 Project Structure

```
LLM-Agent-for-Automated-Code-Auditing/
├── code_auditing_agent.py    # Main agent implementation
├── vulnerable_script.py       # Sample vulnerable code
├── config.yaml                # Configuration file
├── requirements.txt           # Python dependencies
├── .env.example              # Environment template
├── .gitignore                # Git ignore rules
├── README.md                 # This file
└── security_suggestions/     # Generated fix suggestions (created at runtime)
```

## 🔒 Security Note

The `vulnerable_script.py` file contains **intentional security vulnerabilities** for demonstration purposes. **Never use this code in production!** It is designed to showcase the agent's ability to detect and fix common security issues.

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest enhancements
- Submit pull requests

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🎓 Educational Purpose

This project is designed for educational purposes to demonstrate:
- Agentic AI systems using CrewAI
- Custom tool development for AI agents
- Automated security code analysis
- LLM-powered code understanding and generation

## 📚 Resources

- [CrewAI Documentation](https://docs.crewai.com/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [LangChain Documentation](https://python.langchain.com/)
- [Secure Coding Practices](https://owasp.org/www-project-secure-coding-practices-quick-reference-guide/)

## ⚠️ Disclaimer

This tool is for educational and demonstration purposes. Always conduct thorough manual security reviews and testing in addition to automated tools. AI-generated recommendations should be reviewed by security professionals before implementation.