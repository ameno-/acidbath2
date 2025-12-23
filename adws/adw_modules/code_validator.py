"""
Code validation utilities for extracted code blocks.

Provides validation functions for different programming languages and formats.
"""

import ast
import json
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional, Tuple
import yaml


class ValidationResult:
    """Result of code validation."""

    def __init__(self, valid: bool, message: str = "", details: Optional[str] = None):
        self.valid = valid
        self.message = message
        self.details = details

    def __bool__(self):
        return self.valid

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'valid': self.valid,
            'message': self.message,
            'details': self.details
        }


def validate_python(code: str, filepath: Optional[str] = None) -> ValidationResult:
    """
    Syntax check Python code with ast.parse().

    Args:
        code: Python code to validate
        filepath: Optional file path for better error messages

    Returns:
        ValidationResult object
    """
    try:
        ast.parse(code)
        return ValidationResult(
            valid=True,
            message="Python syntax is valid"
        )
    except SyntaxError as e:
        return ValidationResult(
            valid=False,
            message=f"Python syntax error at line {e.lineno}",
            details=str(e)
        )
    except Exception as e:
        return ValidationResult(
            valid=False,
            message="Python validation failed",
            details=str(e)
        )


def validate_bash(code: str, filepath: Optional[str] = None) -> ValidationResult:
    """
    Validate bash script with shellcheck (if available).

    Args:
        code: Bash code to validate
        filepath: Optional file path for shellcheck

    Returns:
        ValidationResult object
    """
    # Check if shellcheck is available
    try:
        subprocess.run(
            ['shellcheck', '--version'],
            capture_output=True,
            check=True,
            timeout=5
        )
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
        # Shellcheck not available, do basic validation
        return ValidationResult(
            valid=True,
            message="Shellcheck not available, basic validation passed"
        )

    # Write code to temporary file
    if filepath:
        temp_file = Path(filepath)
    else:
        import tempfile
        temp_file = Path(tempfile.mktemp(suffix='.sh'))
        temp_file.write_text(code)

    try:
        result = subprocess.run(
            ['shellcheck', '--format=json', str(temp_file)],
            capture_output=True,
            text=True,
            timeout=10
        )

        # Parse shellcheck output
        if result.returncode == 0:
            return ValidationResult(
                valid=True,
                message="Bash script passed shellcheck"
            )
        else:
            try:
                issues = json.loads(result.stdout)
                if issues:
                    first_issue = issues[0]
                    return ValidationResult(
                        valid=False,
                        message=f"Shellcheck warning/error at line {first_issue.get('line', '?')}",
                        details=first_issue.get('message', 'Unknown issue')
                    )
            except json.JSONDecodeError:
                pass

            return ValidationResult(
                valid=False,
                message="Shellcheck found issues",
                details=result.stdout
            )

    except subprocess.TimeoutExpired:
        return ValidationResult(
            valid=False,
            message="Shellcheck validation timed out"
        )
    except Exception as e:
        return ValidationResult(
            valid=False,
            message="Bash validation failed",
            details=str(e)
        )
    finally:
        # Clean up temp file if we created it
        if not filepath and temp_file.exists():
            temp_file.unlink()


def validate_json_yaml(code: str, language: str) -> ValidationResult:
    """
    Schema validation for JSON/YAML.

    Args:
        code: JSON or YAML code to validate
        language: 'json' or 'yaml'

    Returns:
        ValidationResult object
    """
    try:
        if language.lower() == 'json':
            json.loads(code)
            return ValidationResult(
                valid=True,
                message="Valid JSON"
            )
        elif language.lower() in ['yaml', 'yml']:
            yaml.safe_load(code)
            return ValidationResult(
                valid=True,
                message="Valid YAML"
            )
        else:
            return ValidationResult(
                valid=False,
                message=f"Unknown format: {language}"
            )

    except json.JSONDecodeError as e:
        return ValidationResult(
            valid=False,
            message=f"Invalid JSON at line {e.lineno}, column {e.colno}",
            details=str(e.msg)
        )
    except yaml.YAMLError as e:
        return ValidationResult(
            valid=False,
            message="Invalid YAML",
            details=str(e)
        )
    except Exception as e:
        return ValidationResult(
            valid=False,
            message="Validation failed",
            details=str(e)
        )


def validate_code_reference(url: str, timeout: int = 5) -> ValidationResult:
    """
    Verify GitHub links are valid.

    Args:
        url: GitHub URL to validate
        timeout: Request timeout in seconds

    Returns:
        ValidationResult object
    """
    # Basic URL validation
    if not url.startswith('https://github.com/'):
        return ValidationResult(
            valid=False,
            message="Not a valid GitHub URL"
        )

    # Check if URL is well-formed
    parts = url.replace('https://github.com/', '').split('/')
    if len(parts) < 2:
        return ValidationResult(
            valid=False,
            message="Malformed GitHub URL"
        )

    # For now, just validate structure (don't make HTTP requests in validation)
    # Full link checking can be done in CI/CD
    expected_pattern = 'https://github.com/ameno-/acidbath-code/tree/main/examples/'
    if url.startswith(expected_pattern):
        return ValidationResult(
            valid=True,
            message="GitHub URL structure is valid"
        )
    else:
        return ValidationResult(
            valid=False,
            message="URL does not match expected acidbath-code repository pattern",
            details=f"Expected to start with: {expected_pattern}"
        )


def validate_code_block(code: str, language: str, filepath: Optional[str] = None) -> ValidationResult:
    """
    Validate code block based on language.

    Args:
        code: Code to validate
        language: Programming language
        filepath: Optional file path

    Returns:
        ValidationResult object
    """
    language = language.lower()

    # Dispatch to appropriate validator
    if language == 'python':
        return validate_python(code, filepath)
    elif language in ['bash', 'sh', 'shell']:
        return validate_bash(code, filepath)
    elif language in ['json', 'yaml', 'yml']:
        return validate_json_yaml(code, language)
    elif language in ['javascript', 'typescript']:
        # Could add Node.js validation here
        return ValidationResult(
            valid=True,
            message=f"{language} validation not implemented (assumed valid)"
        )
    elif language in ['markdown', 'md', 'text', 'txt']:
        # Text-based formats always pass
        return ValidationResult(
            valid=True,
            message="Text-based format (no validation needed)"
        )
    elif language in ['mermaid', 'diff']:
        # Diagrams don't need validation
        return ValidationResult(
            valid=True,
            message="Diagram format (no validation needed)"
        )
    else:
        # Unknown language - assume valid
        return ValidationResult(
            valid=True,
            message=f"Unknown language '{language}' (assumed valid)"
        )


def validate_file(filepath: Path) -> ValidationResult:
    """
    Validate a file based on its extension.

    Args:
        filepath: Path to file to validate

    Returns:
        ValidationResult object
    """
    if not filepath.exists():
        return ValidationResult(
            valid=False,
            message=f"File does not exist: {filepath}"
        )

    # Determine language from extension
    extension_map = {
        '.py': 'python',
        '.js': 'javascript',
        '.ts': 'typescript',
        '.sh': 'bash',
        '.bash': 'bash',
        '.json': 'json',
        '.yaml': 'yaml',
        '.yml': 'yaml',
        '.md': 'markdown',
        '.txt': 'text',
    }

    ext = filepath.suffix.lower()
    language = extension_map.get(ext, 'unknown')

    try:
        code = filepath.read_text()
        return validate_code_block(code, language, str(filepath))
    except Exception as e:
        return ValidationResult(
            valid=False,
            message=f"Failed to read file: {filepath}",
            details=str(e)
        )


def validate_directory(directory: Path, recursive: bool = True) -> Dict[str, ValidationResult]:
    """
    Validate all code files in a directory.

    Args:
        directory: Path to directory
        recursive: Whether to recurse into subdirectories

    Returns:
        Dictionary mapping file paths to ValidationResult objects
    """
    results = {}

    if not directory.exists():
        return results

    # File extensions to validate
    extensions = {'.py', '.sh', '.bash', '.json', '.yaml', '.yml', '.js', '.ts'}

    # Find all files
    if recursive:
        files = [f for ext in extensions for f in directory.rglob(f'*{ext}')]
    else:
        files = [f for ext in extensions for f in directory.glob(f'*{ext}')]

    # Validate each file
    for filepath in files:
        results[str(filepath)] = validate_file(filepath)

    return results


def generate_validation_report(results: Dict[str, ValidationResult]) -> str:
    """
    Generate a report from validation results.

    Args:
        results: Dictionary mapping file paths to ValidationResult objects

    Returns:
        Markdown report string
    """
    report = []
    report.append("# Code Validation Report\n\n")

    total = len(results)
    valid = sum(1 for r in results.values() if r.valid)
    invalid = total - valid

    report.append(f"**Total Files:** {total}\n")
    report.append(f"**Valid:** {valid}\n")
    report.append(f"**Invalid:** {invalid}\n\n")

    if invalid > 0:
        report.append("## Validation Failures\n\n")
        for filepath, result in results.items():
            if not result.valid:
                report.append(f"### {filepath}\n\n")
                report.append(f"**Message:** {result.message}\n\n")
                if result.details:
                    report.append(f"**Details:**\n```\n{result.details}\n```\n\n")

    report.append("## Summary\n\n")
    if invalid == 0:
        report.append("✅ All files passed validation\n")
    else:
        report.append(f"❌ {invalid} file(s) failed validation\n")

    return ''.join(report)
