"""
Vulnerable Script - Example Code with Security Issues
This script contains intentional security vulnerabilities for demonstration purposes.
"""

import os


def execute_user_command(user_input):
    """
    VULNERABLE: This function executes user input directly without validation.
    This is susceptible to command injection attacks.
    """
    # WARNING: This is a security vulnerability!
    # Never use os.system() with unvalidated user input
    result = os.system(user_input)
    return result


def get_database_connection(db_name):
    """
    VULNERABLE: This function constructs a database query using string concatenation.
    This is susceptible to SQL injection attacks.
    """
    # WARNING: This is a security vulnerability!
    # Never use string concatenation for SQL queries
    query = "SELECT * FROM users WHERE database = '" + db_name + "'"
    return query


def display_user_content(content):
    """
    VULNERABLE: This function displays user content without sanitization.
    This is susceptible to XSS (Cross-Site Scripting) attacks.
    """
    # WARNING: This is a security vulnerability!
    # User content should be sanitized before display
    html_output = f"<div>{content}</div>"
    return html_output


if __name__ == "__main__":
    # Example usage (DO NOT RUN WITH UNTRUSTED INPUT)
    print("This script contains intentional vulnerabilities for audit demonstration.")
    print("Do not use this code in production!")
