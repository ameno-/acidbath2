"""Validation module for ADW import system.

Provides multi-level validation for imported ADW scripts:
- Level 0: Dependencies test (slash command dependencies exist)
- Level 1: Import test (Python syntax and imports)
- Level 2: CLI test (--help or argument parsing)
- Level 3: Dry-run test (full execution without side effects)

Each ADW defines its test criteria in a YAML manifest at adws/manifests/<name>.test.yaml
"""

import os
import sys
import time
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any, Literal

import yaml
from pydantic import BaseModel, Field

from .utils import get_project_root


# Validation level names
ValidationLevel = Literal["dependencies", "import", "cli", "dry_run"]

# ADW categories
ADWCategory = Literal["planning", "building", "testing", "composite", "utility"]


class EffectsConfig(BaseModel):
    """What effects an ADW has when executed."""
    creates_worktree: bool = False
    creates_branch: bool = False
    creates_files: bool = False
    posts_github: bool = False
    creates_commits: bool = False
    creates_pr: bool = False
    modifies_main_repo: bool = False
    runs_tests: bool = False
    allocates_ports: bool = False


class EnvVarsConfig(BaseModel):
    """Environment variables required/optional for an ADW."""
    required: List[str] = Field(default_factory=list)
    optional: List[str] = Field(default_factory=list)


class ImportTestConfig(BaseModel):
    """Configuration for level 1: import test."""
    enabled: bool = True
    timeout: int = 30  # seconds
    command: Optional[str] = None  # Custom import command (if not using default)


class CLITestConfig(BaseModel):
    """Configuration for level 2: CLI test."""
    enabled: bool = True
    command: Optional[str] = "--help"  # Can be None for modules/disabled tests
    exit_code: int = 0
    timeout: int = 30  # seconds
    expected_output: Optional[List[str]] = None


class DryRunConfig(BaseModel):
    """Configuration for level 3: dry-run test."""
    enabled: bool = False
    args: List[str] = Field(default_factory=list)  # List of args
    command: Optional[str] = None  # Alternative: single command string (will be split)
    exit_code: int = 0
    timeout: int = 120  # seconds
    expected_output: Optional[List[str]] = None


class ValidationConfig(BaseModel):
    """Validation configuration for all levels."""
    import_test: ImportTestConfig = Field(default_factory=ImportTestConfig)
    cli_test: CLITestConfig = Field(default_factory=CLITestConfig)
    dry_run: DryRunConfig = Field(default_factory=DryRunConfig)


class DocumentationConfig(BaseModel):
    """Documentation metadata for README updates."""
    usage_example: Optional[str] = None
    related_adws: List[str] = Field(default_factory=list)
    workflow_sequence: Optional[int] = None


class ManifestSchema(BaseModel):
    """Complete YAML manifest schema for an ADW."""
    model_config = {"extra": "ignore"}  # Ignore extra fields for forward compatibility

    name: str
    description: str
    category: ADWCategory = "utility"
    type: Optional[str] = None  # "module" for utility modules, None for ADW scripts
    version: str = "1.0.0"
    effects: EffectsConfig = Field(default_factory=EffectsConfig)
    module_dependencies: List[str] = Field(default_factory=list)
    external_dependencies: List[str] = Field(default_factory=list)  # For fastapi, etc.
    slash_command_dependencies: List[str] = Field(default_factory=list)  # Required slash commands
    env_vars: EnvVarsConfig = Field(default_factory=EnvVarsConfig)
    validation: ValidationConfig = Field(default_factory=ValidationConfig)
    documentation: DocumentationConfig = Field(default_factory=DocumentationConfig)


class ValidationResult(BaseModel):
    """Result of a single validation level."""
    level: int
    name: ValidationLevel
    passed: bool
    message: str
    duration_ms: int
    output: Optional[str] = None
    skipped: bool = False
    skip_reason: Optional[str] = None


class ValidationReport(BaseModel):
    """Complete validation report for an ADW."""
    adw_name: str
    adw_path: str
    manifest_path: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)
    results: List[ValidationResult] = Field(default_factory=list)
    overall_passed: bool = False
    highest_level_passed: int = 0

    def summary(self) -> str:
        """Generate a summary string of validation results."""
        lines = [f"Validation Report: {self.adw_name}"]
        lines.append("-" * 40)

        for result in self.results:
            status = "PASS" if result.passed else ("SKIP" if result.skipped else "FAIL")
            lines.append(f"Level {result.level} ({result.name}): {status} ({result.duration_ms}ms)")
            if not result.passed and result.message:
                lines.append(f"  -> {result.message[:100]}")

        lines.append("-" * 40)
        overall = "PASSED" if self.overall_passed else "FAILED"
        lines.append(f"Overall: {overall} (highest level: {self.highest_level_passed})")

        return "\n".join(lines)


def get_manifests_dir() -> Path:
    """Get the path to the manifests directory."""
    return Path(get_project_root()) / "adws" / "manifests"


def load_manifest(manifest_path: str) -> ManifestSchema:
    """Load and validate a YAML manifest.

    Args:
        manifest_path: Path to the YAML manifest file

    Returns:
        Parsed ManifestSchema

    Raises:
        FileNotFoundError: If manifest file doesn't exist
        ValueError: If manifest is invalid
    """
    if not os.path.exists(manifest_path):
        raise FileNotFoundError(f"Manifest not found: {manifest_path}")

    with open(manifest_path, "r") as f:
        data = yaml.safe_load(f)

    if data is None:
        raise ValueError(f"Empty manifest: {manifest_path}")

    return ManifestSchema(**data)


def find_manifest_for_adw(adw_path: str) -> Optional[str]:
    """Find the manifest file for an ADW.

    Args:
        adw_path: Path to the ADW script

    Returns:
        Path to manifest file if found, None otherwise
    """
    adw_name = Path(adw_path).stem
    manifests_dir = get_manifests_dir()

    # Try different naming conventions
    candidates = [
        manifests_dir / f"{adw_name}.test.yaml",
        manifests_dir / f"{adw_name}.yaml",
        manifests_dir / f"{adw_name}.manifest.yaml",
    ]

    for candidate in candidates:
        if candidate.exists():
            return str(candidate)

    return None


def generate_manifest_template(adw_path: str) -> str:
    """Generate a manifest template for an ADW by analyzing the script.

    Args:
        adw_path: Path to the ADW script

    Returns:
        YAML string for the manifest template
    """
    adw_name = Path(adw_path).stem

    # Try to extract description from docstring
    description = f"AI Developer Workflow: {adw_name}"
    try:
        with open(adw_path, "r") as f:
            content = f.read()
            # Look for module docstring
            if '"""' in content:
                start = content.find('"""') + 3
                end = content.find('"""', start)
                if end > start:
                    docstring = content[start:end].strip()
                    first_line = docstring.split("\n")[0]
                    if first_line:
                        description = first_line
    except Exception:
        pass

    # Detect category from name
    category = "utility"
    if "plan" in adw_name:
        category = "planning"
    elif "build" in adw_name or "implement" in adw_name:
        category = "building"
    elif "test" in adw_name:
        category = "testing"
    elif any(x in adw_name for x in ["plan_build", "sdlc", "ship"]):
        category = "composite"

    # Detect if it has major effects
    has_major_effects = any(x in adw_name for x in ["iso", "plan", "build", "ship"])

    manifest = ManifestSchema(
        name=adw_name,
        description=description,
        category=category,
        effects=EffectsConfig(
            creates_worktree="iso" in adw_name,
            creates_branch="iso" in adw_name or "plan" in adw_name,
            creates_files=True,
            posts_github="iso" in adw_name,
            creates_commits="iso" in adw_name or "build" in adw_name,
        ),
        module_dependencies=[
            "adw_modules.agent",
            "adw_modules.state",
            "adw_modules.utils",
        ],
        env_vars=EnvVarsConfig(
            required=["ANTHROPIC_API_KEY"],
            optional=["GITHUB_PAT"],
        ),
        validation=ValidationConfig(
            import_test=ImportTestConfig(enabled=True),
            cli_test=CLITestConfig(enabled=True),
            dry_run=DryRunConfig(enabled=has_major_effects),
        ),
        documentation=DocumentationConfig(
            usage_example=f"uv run {adw_name}.py [args]",
        ),
    )

    return yaml.dump(manifest.model_dump(), default_flow_style=False, sort_keys=False)


def validate_level_0_dependencies(adw_path: str, manifest: Optional[ManifestSchema] = None) -> ValidationResult:
    """Run level 0 validation: Slash command dependencies exist.

    Args:
        adw_path: Path to the ADW script
        manifest: Optional manifest for configuration

    Returns:
        ValidationResult for level 0
    """
    start_time = time.time()

    # If no manifest or no slash command dependencies, skip
    if manifest is None or not manifest.slash_command_dependencies:
        return ValidationResult(
            level=0,
            name="dependencies",
            passed=True,
            message="No slash command dependencies declared",
            duration_ms=0,
            skipped=True,
            skip_reason="No dependencies in manifest",
        )

    project_root = get_project_root()
    commands_dir = Path(project_root) / ".claude" / "commands"

    missing_commands = []
    for cmd_name in manifest.slash_command_dependencies:
        # Check if command file exists (without leading /)
        cmd_file = commands_dir / f"{cmd_name}.md"
        if not cmd_file.exists():
            missing_commands.append(cmd_name)

    duration_ms = int((time.time() - start_time) * 1000)

    if missing_commands:
        return ValidationResult(
            level=0,
            name="dependencies",
            passed=False,
            message=f"Missing slash commands: {', '.join(missing_commands)}",
            duration_ms=duration_ms,
            output=f"Expected in: {commands_dir}",
        )

    return ValidationResult(
        level=0,
        name="dependencies",
        passed=True,
        message=f"All {len(manifest.slash_command_dependencies)} slash command dependencies found",
        duration_ms=duration_ms,
    )


def validate_level_1_import(adw_path: str, manifest: Optional[ManifestSchema] = None) -> ValidationResult:
    """Run level 1 validation: Python import test.

    Args:
        adw_path: Path to the ADW script
        manifest: Optional manifest for configuration

    Returns:
        ValidationResult for level 1
    """
    timeout = 30
    if manifest and manifest.validation.import_test:
        if not manifest.validation.import_test.enabled:
            return ValidationResult(
                level=1,
                name="import",
                passed=True,
                message="Import test disabled",
                duration_ms=0,
                skipped=True,
                skip_reason="Disabled in manifest",
            )
        timeout = manifest.validation.import_test.timeout

    start_time = time.time()

    adw_name = Path(adw_path).stem
    project_root = get_project_root()

    # Build import command based on ADW location
    if "adw_modules" in adw_path:
        # Module import
        module_name = adw_name
        import_cmd = f"from adws.adw_modules.{module_name} import *"
    else:
        # ADW script import
        import_cmd = f"from adws.{adw_name} import main"

    cmd = [
        "python3", "-c",
        f"import sys; sys.path.insert(0, '{project_root}'); {import_cmd}; print('OK')"
    ]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=project_root,
        )

        duration_ms = int((time.time() - start_time) * 1000)

        if result.returncode == 0:
            return ValidationResult(
                level=1,
                name="import",
                passed=True,
                message="Import successful",
                duration_ms=duration_ms,
                output=result.stdout.strip(),
            )
        else:
            return ValidationResult(
                level=1,
                name="import",
                passed=False,
                message=f"Import failed: {result.stderr[:200]}",
                duration_ms=duration_ms,
                output=result.stderr,
            )

    except subprocess.TimeoutExpired:
        duration_ms = int((time.time() - start_time) * 1000)
        return ValidationResult(
            level=1,
            name="import",
            passed=False,
            message=f"Import timed out after {timeout}s",
            duration_ms=duration_ms,
        )
    except Exception as e:
        duration_ms = int((time.time() - start_time) * 1000)
        return ValidationResult(
            level=1,
            name="import",
            passed=False,
            message=f"Import error: {str(e)}",
            duration_ms=duration_ms,
        )


def validate_level_2_cli(adw_path: str, manifest: Optional[ManifestSchema] = None) -> ValidationResult:
    """Run level 2 validation: CLI help test.

    Args:
        adw_path: Path to the ADW script
        manifest: Optional manifest for configuration

    Returns:
        ValidationResult for level 2
    """
    config = CLITestConfig()
    if manifest and manifest.validation.cli_test:
        if not manifest.validation.cli_test.enabled:
            return ValidationResult(
                level=2,
                name="cli",
                passed=True,
                message="CLI test disabled",
                duration_ms=0,
                skipped=True,
                skip_reason="Disabled in manifest",
            )
        config = manifest.validation.cli_test

    start_time = time.time()
    project_root = get_project_root()

    cmd = ["uv", "run", adw_path, config.command]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=config.timeout,
            cwd=project_root,
        )

        duration_ms = int((time.time() - start_time) * 1000)

        # Check exit code
        if result.returncode != config.exit_code:
            return ValidationResult(
                level=2,
                name="cli",
                passed=False,
                message=f"Exit code {result.returncode}, expected {config.exit_code}",
                duration_ms=duration_ms,
                output=result.stderr[:500] if result.stderr else result.stdout[:500],
            )

        # Check expected output if specified
        if config.expected_output:
            output = result.stdout + result.stderr
            for expected in config.expected_output:
                if expected not in output:
                    return ValidationResult(
                        level=2,
                        name="cli",
                        passed=False,
                        message=f"Expected output not found: '{expected}'",
                        duration_ms=duration_ms,
                        output=output[:500],
                    )

        return ValidationResult(
            level=2,
            name="cli",
            passed=True,
            message="CLI test successful",
            duration_ms=duration_ms,
            output=result.stdout[:200] if result.stdout else None,
        )

    except subprocess.TimeoutExpired:
        duration_ms = int((time.time() - start_time) * 1000)
        return ValidationResult(
            level=2,
            name="cli",
            passed=False,
            message=f"CLI test timed out after {config.timeout}s",
            duration_ms=duration_ms,
        )
    except Exception as e:
        duration_ms = int((time.time() - start_time) * 1000)
        return ValidationResult(
            level=2,
            name="cli",
            passed=False,
            message=f"CLI error: {str(e)}",
            duration_ms=duration_ms,
        )


def validate_level_3_dry_run(adw_path: str, manifest: Optional[ManifestSchema] = None) -> ValidationResult:
    """Run level 3 validation: Dry-run execution.

    Args:
        adw_path: Path to the ADW script
        manifest: Optional manifest for configuration

    Returns:
        ValidationResult for level 3
    """
    config = DryRunConfig()
    if manifest and manifest.validation.dry_run:
        if not manifest.validation.dry_run.enabled:
            return ValidationResult(
                level=3,
                name="dry_run",
                passed=True,
                message="Dry-run test disabled",
                duration_ms=0,
                skipped=True,
                skip_reason="Disabled in manifest",
            )
        config = manifest.validation.dry_run

    start_time = time.time()
    project_root = get_project_root()

    # Build command - prefer command string over args list
    if config.command:
        # Split command string into args
        cmd = ["uv", "run", adw_path] + config.command.split()
    else:
        cmd = ["uv", "run", adw_path] + config.args

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=config.timeout,
            cwd=project_root,
        )

        duration_ms = int((time.time() - start_time) * 1000)

        # Check exit code
        if result.returncode != config.exit_code:
            return ValidationResult(
                level=3,
                name="dry_run",
                passed=False,
                message=f"Exit code {result.returncode}, expected {config.exit_code}",
                duration_ms=duration_ms,
                output=result.stderr[:500] if result.stderr else result.stdout[:500],
            )

        # Check expected output if specified
        if config.expected_output:
            output = result.stdout + result.stderr
            for expected in config.expected_output:
                if expected not in output:
                    return ValidationResult(
                        level=3,
                        name="dry_run",
                        passed=False,
                        message=f"Expected output not found: '{expected}'",
                        duration_ms=duration_ms,
                        output=output[:500],
                    )

        return ValidationResult(
            level=3,
            name="dry_run",
            passed=True,
            message="Dry-run successful",
            duration_ms=duration_ms,
            output=result.stdout[:200] if result.stdout else None,
        )

    except subprocess.TimeoutExpired:
        duration_ms = int((time.time() - start_time) * 1000)
        return ValidationResult(
            level=3,
            name="dry_run",
            passed=False,
            message=f"Dry-run timed out after {config.timeout}s",
            duration_ms=duration_ms,
        )
    except Exception as e:
        duration_ms = int((time.time() - start_time) * 1000)
        return ValidationResult(
            level=3,
            name="dry_run",
            passed=False,
            message=f"Dry-run error: {str(e)}",
            duration_ms=duration_ms,
        )


def run_validation(
    adw_path: str,
    manifest: Optional[ManifestSchema] = None,
    max_level: int = 3,
    stop_on_failure: bool = False,
) -> ValidationReport:
    """Run validation levels on an ADW.

    Args:
        adw_path: Path to the ADW script
        manifest: Optional manifest for configuration
        max_level: Maximum validation level to run (0, 1, 2, or 3)
        stop_on_failure: Stop at first failure if True

    Returns:
        ValidationReport with all results
    """
    adw_name = Path(adw_path).stem
    manifest_path = find_manifest_for_adw(adw_path) if manifest is None else None

    if manifest is None and manifest_path:
        try:
            manifest = load_manifest(manifest_path)
        except Exception:
            manifest = None

    report = ValidationReport(
        adw_name=adw_name,
        adw_path=adw_path,
        manifest_path=manifest_path,
    )

    # Level 0: Dependencies test (always run first)
    if max_level >= 0:
        result = validate_level_0_dependencies(adw_path, manifest)
        report.results.append(result)
        if result.passed and not result.skipped:
            report.highest_level_passed = 0
        if not result.passed and stop_on_failure:
            report.overall_passed = False
            return report

    # Level 1: Import test
    if max_level >= 1:
        result = validate_level_1_import(adw_path, manifest)
        report.results.append(result)
        if result.passed and not result.skipped:
            report.highest_level_passed = 1
        if not result.passed and stop_on_failure:
            report.overall_passed = False
            return report

    # Level 2: CLI test
    if max_level >= 2:
        result = validate_level_2_cli(adw_path, manifest)
        report.results.append(result)
        if result.passed and not result.skipped:
            report.highest_level_passed = 2
        if not result.passed and stop_on_failure:
            report.overall_passed = False
            return report

    # Level 3: Dry-run test
    if max_level >= 3:
        result = validate_level_3_dry_run(adw_path, manifest)
        report.results.append(result)
        if result.passed and not result.skipped:
            report.highest_level_passed = 3

    # Determine overall pass/fail
    # Pass if all non-skipped tests passed
    non_skipped_results = [r for r in report.results if not r.skipped]
    report.overall_passed = all(r.passed for r in non_skipped_results) if non_skipped_results else True

    return report
