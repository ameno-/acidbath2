#!/usr/bin/env -S uv run
# /// script
# dependencies = ["click", "rich", "pytest", "pytest-cov", "pytest-xdist"]
# ///

"""
Test Runner CLI - Module-based test execution with coverage and timing analysis.

Usage:
  uv run adws/run_tests.py                      # Run all tests
  uv run adws/run_tests.py -m agent -m git_ops  # Run specific modules
  uv run adws/run_tests.py --coverage           # With coverage report
  uv run adws/run_tests.py --timing             # With timing analysis
  uv run adws/run_tests.py list                 # List available modules
  uv run adws/run_tests.py stats                # Show test statistics
"""

import os
import sys
import time
import json
import subprocess
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from datetime import datetime

import click

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Constants
PROJECT_ROOT = Path(__file__).parent.parent
TESTS_DIR = PROJECT_ROOT / "tests" / "modules"


@dataclass
class ModuleResult:
    """Result of running tests for a single module."""
    name: str
    test_file: str
    tests_collected: int = 0
    passed: int = 0
    failed: int = 0
    skipped: int = 0
    errors: int = 0
    duration: float = 0.0
    failures: List[Dict] = field(default_factory=list)


@dataclass
class TestRunResult:
    """Result of a complete test run."""
    modules: List[ModuleResult] = field(default_factory=list)
    total_duration: float = 0.0
    coverage_data: Optional[Dict] = None
    timing_data: Optional[Dict] = None

    @property
    def total_tests(self) -> int:
        return sum(m.tests_collected for m in self.modules)

    @property
    def total_passed(self) -> int:
        return sum(m.passed for m in self.modules)

    @property
    def total_failed(self) -> int:
        return sum(m.failed for m in self.modules)

    @property
    def total_skipped(self) -> int:
        return sum(m.skipped for m in self.modules)

    @property
    def total_errors(self) -> int:
        return sum(m.errors for m in self.modules)

    @property
    def success(self) -> bool:
        return self.total_failed == 0 and self.total_errors == 0


def discover_modules() -> Dict[str, Path]:
    """Auto-discover test modules from tests/modules/ directory."""
    modules = {}
    if TESTS_DIR.exists():
        for test_file in sorted(TESTS_DIR.glob("test_*.py")):
            # Extract module name from test_<name>.py
            module_name = test_file.stem[5:]  # Remove "test_" prefix
            modules[module_name] = test_file
    return modules


def count_tests_in_module(test_file: Path) -> int:
    """Count the number of test functions in a test file."""
    try:
        result = subprocess.run(
            ["uv", "run", "pytest", str(test_file), "--collect-only", "-q"],
            capture_output=True,
            text=True,
            cwd=PROJECT_ROOT,
        )
        # Parse output - look for "collected N items" line
        for line in result.stdout.splitlines():
            if "collected" in line and "item" in line:
                # Format: "collected 37 items"
                parts = line.split()
                for i, part in enumerate(parts):
                    if part == "collected" and i + 1 < len(parts):
                        try:
                            return int(parts[i + 1])
                        except ValueError:
                            pass
        return 0
    except Exception:
        return 0


def run_module_tests(
    module_name: str,
    test_file: Path,
    coverage: bool = False,
    fail_fast: bool = False,
    parallel: Optional[int] = None,
) -> ModuleResult:
    """Run tests for a single module using pytest."""
    start_time = time.time()

    # Build pytest command
    cmd = ["uv", "run", "pytest", str(test_file), "-v", "--tb=short"]

    if coverage:
        cmd.extend([f"--cov=adws/adw_modules/{module_name}", "--cov-report="])

    if fail_fast:
        cmd.append("-x")

    if parallel and parallel > 1:
        cmd.extend(["-n", str(parallel)])

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=PROJECT_ROOT,
        )

        duration = time.time() - start_time

        # Parse stdout to extract results
        return parse_pytest_output(module_name, str(test_file), result.stdout, duration)

    except Exception as e:
        return ModuleResult(
            name=module_name,
            test_file=str(test_file),
            errors=1,
            duration=time.time() - start_time,
            failures=[{"name": "execution", "outcome": "error", "message": str(e)}],
        )


def parse_pytest_output(module_name: str, test_file: str, stdout: str, duration: float) -> ModuleResult:
    """Parse pytest stdout to extract test results."""
    passed = failed = skipped = errors = 0
    total = 0

    for line in stdout.splitlines():
        line = line.strip()
        # Parse summary line like "10 passed, 2 failed, 1 skipped"
        if " passed" in line or " failed" in line or " skipped" in line:
            parts = line.replace(",", " ").split()
            i = 0
            while i < len(parts):
                if parts[i].isdigit() and i + 1 < len(parts):
                    count = int(parts[i])
                    status = parts[i + 1]
                    if "passed" in status:
                        passed = count
                    elif "failed" in status:
                        failed = count
                    elif "skipped" in status:
                        skipped = count
                    elif "error" in status:
                        errors = count
                    i += 2
                else:
                    i += 1

    total = passed + failed + skipped + errors

    return ModuleResult(
        name=module_name,
        test_file=test_file,
        tests_collected=total,
        passed=passed,
        failed=failed,
        skipped=skipped,
        errors=errors,
        duration=duration,
    )


def collect_coverage_data(modules: List[str]) -> Dict:
    """Collect coverage data for specified modules."""
    source_paths = [f"adws/adw_modules/{m}.py" for m in modules if (PROJECT_ROOT / "adws" / "adw_modules" / f"{m}.py").exists()]

    if not source_paths:
        return {}

    # Run pytest with coverage
    cmd = [
        "uv", "run", "pytest", "tests/modules/",
        f"--cov={'--cov='.join([''] + source_paths)}".replace("--cov=--cov=", "--cov="),
        "--cov-report=json",
        "-q",
    ]

    # Actually run with proper cov args
    cov_args = []
    for path in source_paths:
        cov_args.extend(["--cov", path.replace("adws/adw_modules/", "adws.adw_modules.").replace(".py", "")])

    cmd = ["uv", "run", "pytest", "tests/modules/", *cov_args, "--cov-report=json", "-q"]

    try:
        subprocess.run(cmd, capture_output=True, cwd=PROJECT_ROOT)

        cov_file = PROJECT_ROOT / "coverage.json"
        if cov_file.exists():
            with open(cov_file) as f:
                data = json.load(f)
            cov_file.unlink()
            return data
    except Exception:
        pass

    return {}


def collect_timing_data(test_result: TestRunResult) -> Dict:
    """Collect timing data from test results."""
    by_module = {}
    slowest_tests = []

    for module in test_result.modules:
        by_module[module.name] = {
            "tests": module.tests_collected,
            "total": module.duration,
            "avg": module.duration / max(module.tests_collected, 1),
            "max": module.duration,  # Would need per-test timing for accurate max
        }

    return {
        "by_module": by_module,
        "slowest_tests": slowest_tests,
        "total_duration": test_result.total_duration,
    }


# Output formatters

def format_header(title: str, char: str = "=", width: int = 80) -> str:
    """Format a section header."""
    return f"{char * width}\n{title}\n{char * width}"


def format_run_header() -> str:
    """Format the test run header."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return format_header(f"TEST RUN: {timestamp}")


def format_module_row(index: int, total: int, result: ModuleResult) -> str:
    """Format a single module result row."""
    name = result.name
    dots = "." * max(1, 35 - len(name))

    if result.failed > 0 or result.errors > 0:
        status = "FAIL"
    elif result.skipped > 0 and result.passed == 0:
        status = "SKIP"
    else:
        status = "PASS"

    return f"[{index:3d}/{total:3d}] {name} {dots} {result.tests_collected:3d} tests   {status:4s}    {result.duration:5.1f}s"


def format_summary(result: TestRunResult) -> str:
    """Format the summary section."""
    lines = [
        "",
        format_header("SUMMARY"),
        "",
        f"Total Tests:    {result.total_tests}",
        f"Passed:         {result.total_passed}",
        f"Failed:         {result.total_failed}",
        f"Skipped:        {result.total_skipped}",
        f"Errors:         {result.total_errors}",
        f"Duration:       {result.total_duration:.1f}s",
        "",
    ]

    if result.success:
        lines.append("Status: ALL TESTS PASSED")
    else:
        lines.append("Status: TESTS FAILED")

    return "\n".join(lines)


def format_coverage_report(coverage_data: Dict) -> str:
    """Format coverage report as plain text."""
    if not coverage_data:
        return ""

    files = coverage_data.get("files", {})
    if not files:
        return ""

    lines = [
        "",
        format_header("COVERAGE REPORT"),
        "",
        "Module Coverage:",
    ]

    total_covered = 0
    total_lines = 0

    for filepath, data in sorted(files.items()):
        if "adw_modules" not in filepath:
            continue

        name = Path(filepath).name
        summary = data.get("summary", {})
        covered = summary.get("covered_lines", 0)
        total = summary.get("num_statements", 0)
        pct = (covered / total * 100) if total > 0 else 0

        total_covered += covered
        total_lines += total

        dots = "." * max(1, 40 - len(name))
        lines.append(f"  {name} {dots} {pct:5.1f}%   ({covered}/{total} lines)")

    overall_pct = (total_covered / total_lines * 100) if total_lines > 0 else 0
    lines.extend([
        "",
        "-" * 80,
        f"Overall Coverage: {overall_pct:.1f}% ({total_covered}/{total_lines} lines)",
        "-" * 80,
    ])

    return "\n".join(lines)


def format_timing_report(timing_data: Dict) -> str:
    """Format timing analysis as plain text."""
    if not timing_data:
        return ""

    lines = [
        "",
        format_header("TIMING ANALYSIS"),
        "",
        "Module Timing Breakdown:",
        "  Module                Tests   Total     Avg",
        "  " + "-" * 50,
    ]

    for module, data in sorted(timing_data.get("by_module", {}).items(), key=lambda x: -x[1]["total"]):
        lines.append(
            f"  {module:22s} {data['tests']:3d}   {data['total']:5.2f}s   {data['avg']:5.3f}s"
        )

    lines.extend([
        "  " + "-" * 50,
        f"  Total Execution Time: {timing_data.get('total_duration', 0):.2f}s",
    ])

    return "\n".join(lines)


def format_failure_details(result: TestRunResult) -> str:
    """Format detailed failure information."""
    failures = []
    for module in result.modules:
        for failure in module.failures:
            failures.append((module.name, failure))

    if not failures:
        return ""

    lines = [
        "",
        format_header("FAILURE DETAILS"),
    ]

    for module_name, failure in failures:
        lines.extend([
            "",
            f"FAILED: {module_name}::{failure.get('name', 'unknown')}",
            "-" * 80,
        ])

        message = failure.get("message", "")
        if message:
            # Truncate long messages
            if len(message) > 500:
                message = message[:500] + "\n... (truncated)"
            lines.append(message)

        lines.append("")

    return "\n".join(lines)


def format_module_list(modules: Dict[str, Path]) -> str:
    """Format the list of available modules."""
    lines = [
        format_header("AVAILABLE TEST MODULES"),
        "",
        f"{'Module':<25} {'Tests':>6}   Source",
        "-" * 80,
    ]

    total_tests = 0
    for name, path in sorted(modules.items()):
        count = count_tests_in_module(path)
        total_tests += count
        source = f"adws/adw_modules/{name}.py"
        lines.append(f"{name:<25} {count:>6}   {source}")

    lines.extend([
        "-" * 80,
        f"Total: {len(modules)} modules, {total_tests} tests",
    ])

    return "\n".join(lines)


def format_stats(modules: Dict[str, Path]) -> str:
    """Format quick test statistics."""
    lines = [
        format_header("TEST STATISTICS"),
        "",
    ]

    total_tests = 0
    module_counts = []

    for name, path in sorted(modules.items()):
        count = count_tests_in_module(path)
        total_tests += count
        module_counts.append((name, count))

    lines.append(f"Total Modules:  {len(modules)}")
    lines.append(f"Total Tests:    {total_tests}")
    lines.append("")
    lines.append("Tests by Module:")

    for name, count in sorted(module_counts, key=lambda x: -x[1]):
        bar = "#" * (count // 5)
        lines.append(f"  {name:<22} {count:>3}  {bar}")

    return "\n".join(lines)


# CLI Commands

@click.group(invoke_without_command=True)
@click.option("--module", "-m", multiple=True, help="Module(s) to test (can be repeated)")
@click.option("--coverage", is_flag=True, help="Enable coverage reporting")
@click.option("--timing", is_flag=True, help="Show timing analysis")
@click.option("--verbose", "-v", is_flag=True, help="Verbose output")
@click.option("--fail-fast", "-x", is_flag=True, help="Stop on first failure")
@click.option("--parallel", "-n", type=int, default=None, help="Parallel workers")
@click.pass_context
def cli(ctx, module, coverage, timing, verbose, fail_fast, parallel):
    """Test Runner CLI for Jerry project.

    Run tests by module with coverage and timing analysis.
    Output is plain text, optimized for CI/PR reviews.
    """
    if ctx.invoked_subcommand is None:
        # Run tests directly with provided options
        ctx.invoke(run_cmd, module=module, coverage=coverage, timing=timing,
                   verbose=verbose, fail_fast=fail_fast, parallel=parallel)


@cli.command("run")
@click.option("--module", "-m", multiple=True, help="Module(s) to test (can be repeated)")
@click.option("--coverage", is_flag=True, help="Enable coverage reporting")
@click.option("--timing", is_flag=True, help="Show timing analysis")
@click.option("--verbose", "-v", is_flag=True, help="Verbose output")
@click.option("--fail-fast", "-x", is_flag=True, help="Stop on first failure")
@click.option("--parallel", "-n", type=int, default=None, help="Parallel workers")
def run_cmd(module, coverage, timing, verbose, fail_fast, parallel):
    """Run tests for specified modules (or all if none specified)."""
    all_modules = discover_modules()

    if not all_modules:
        click.echo("No test modules found in tests/modules/")
        sys.exit(1)

    # Filter modules if specified
    if module:
        selected_modules = {}
        for m in module:
            if m in all_modules:
                selected_modules[m] = all_modules[m]
            else:
                click.echo(f"Warning: Module '{m}' not found, skipping")
        if not selected_modules:
            click.echo("No valid modules specified")
            sys.exit(1)
    else:
        selected_modules = all_modules

    # Print header
    click.echo(format_run_header())
    click.echo("")
    click.echo(f"Configuration:")
    click.echo(f"  Modules: {len(selected_modules)} of {len(all_modules)}")
    click.echo(f"  Coverage: {'enabled' if coverage else 'disabled'}")
    click.echo(f"  Parallel: {parallel if parallel else 'sequential'}")
    click.echo("")
    click.echo("-" * 80)
    click.echo("RUNNING TESTS")
    click.echo("-" * 80)
    click.echo("")

    # Run tests
    start_time = time.time()
    result = TestRunResult()
    total_modules = len(selected_modules)

    for i, (name, path) in enumerate(sorted(selected_modules.items()), 1):
        module_result = run_module_tests(name, path, coverage, fail_fast, parallel)
        result.modules.append(module_result)

        # Print progress
        row = format_module_row(i, total_modules, module_result)
        click.echo(row)

        # Stop early if fail-fast and failure
        if fail_fast and (module_result.failed > 0 or module_result.errors > 0):
            click.echo("\nStopping due to --fail-fast")
            break

    result.total_duration = time.time() - start_time

    # Print summary
    click.echo(format_summary(result))

    # Print failure details if any
    if result.total_failed > 0 or result.total_errors > 0:
        click.echo(format_failure_details(result))

    # Print timing analysis if requested
    if timing:
        timing_data = collect_timing_data(result)
        result.timing_data = timing_data
        click.echo(format_timing_report(timing_data))

    # Print coverage if requested
    if coverage:
        click.echo("\nCollecting coverage data...")
        coverage_data = collect_coverage_data(list(selected_modules.keys()))
        if coverage_data:
            result.coverage_data = coverage_data
            click.echo(format_coverage_report(coverage_data))

    # Exit with appropriate code
    sys.exit(0 if result.success else 1)


@cli.command("list")
def list_cmd():
    """List available test modules."""
    modules = discover_modules()

    if not modules:
        click.echo("No test modules found in tests/modules/")
        sys.exit(1)

    click.echo(format_module_list(modules))


@cli.command("stats")
def stats_cmd():
    """Show test statistics."""
    modules = discover_modules()

    if not modules:
        click.echo("No test modules found in tests/modules/")
        sys.exit(1)

    click.echo(format_stats(modules))


if __name__ == "__main__":
    cli()
