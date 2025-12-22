# Chore: Jerry Validation Slash Command Test

## Metadata
adw_id: `53fe41e6`
prompt: `Jerry validation slash command test`

## Chore Description
Create a comprehensive test to validate that the Jerry validation workflow functions correctly when executed through a slash command. This test specifically validates the Level 3 workflow test in `jerry_validate.py` which executes the `/chore` slash command. The test should verify that:

1. The `adw_slash_command.py` script executes successfully with the `/chore` command
2. The `/chore` command accepts arguments and processes them correctly
3. A spec file is created in the `specs/` directory with the correct format
4. The execution produces proper output files in the `agents/` directory
5. The validation can detect success/failure conditions accurately

This chore is critical for ensuring that Jerry's validation system (specifically Level 3 validation in `jerry_validate.py` line 352) works correctly and can be used to validate Jerry installations in production environments. The Level 3 validation test at lines 344-373 executes:

```bash
./adws/adw_slash_command.py /chore "Jerry validation slash command test"
```

This chore will implement improvements to ensure this test provides comprehensive coverage and reliable results.

## Relevant Files
Use these files to complete the chore:

- `/Users/ameno/dev/acidbath2/adws/jerry_validate.py` - Contains Level 3 validation that tests slash command execution (lines 418-446); the main validation logic
- `/Users/ameno/dev/acidbath2/adws/adw_slash_command.py` - The script that executes slash commands; handles template loading and argument passing
- `/Users/ameno/dev/acidbath2/.claude/commands/chore.md` - The slash command template that defines the chore planning workflow
- `/Users/ameno/dev/acidbath2/adws/adw_modules/agent.py` - Core agent execution logic used by adw_slash_command.py
- `/Users/ameno/dev/acidbath2/adws/adw_modules/validation.py` - Validation module for ADW import system with multi-level validation
- `/Users/ameno/dev/acidbath2/specs/` - Directory where chore plan output is created
- `/Users/ameno/dev/acidbath2/agents/` - Directory where agent execution outputs are stored
- `/Users/ameno/dev/acidbath2/.jerry/manifest.json` - Contains manifest data about required files and directories

### New Files
- `/Users/ameno/dev/acidbath2/tests/test_validation_slash_command.py` - Integration test for comprehensive slash command validation (optional but recommended)

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### 1. Review Current Validation Implementation
- Read the current Level 3 validation test for slash commands in `jerry_validate.py` (lines 344-373)
- Understand the test expectations: command execution, returncode check, specs directory check, timeout handling
- Identify the test parameters: subprocess execution with 120s timeout, output capture
- Note the current validation checks: returncode == 0, specs/ directory exists

### 2. Verify Prerequisites and Dependencies
- Confirm `adws/jerry_validate.py` exists and is executable
- Verify `adws/adw_slash_command.py` exists and can execute with --help flag
- Check that `.claude/commands/chore.md` template exists and is readable
- Ensure Python dependencies are available: click, rich, pydantic, python-dotenv
- Verify Claude Code CLI is installed and accessible

### 3. Execute Level 3 Validation Test
- Run: `uv run /Users/ameno/dev/acidbath2/adws/jerry_validate.py --level 3`
- Monitor the output for the slash command test result (lines 418-446 in validation script)
- Capture the return code (should be 0 for success)
- Note any error messages or timeout issues
- Verify the validation reports "Slash command executed successfully"

### 4. Verify Output Directory Structure and Content
- Check that `agents/` directory exists and contains execution output
- Locate the most recent execution in `agents/<adw_id>/executor/`
- Verify the output structure contains all expected files:
  - `cc_raw_output.jsonl` - Raw streaming output from Claude Code
  - `cc_raw_output.json` - All messages as JSON array
  - `cc_final_object.json` - Last message entry (final result)
  - `custom_summary_output.json` - High-level execution summary with metadata
- Inspect `custom_summary_output.json` for expected fields: success, session_id, slash_command, args

### 5. Examine Generated Chore Plan Spec File
- Find the newly generated chore plan file in `specs/` directory
- Expected filename pattern: `chore-<adw_id>-jerry-validation-slash-command-test.md`
- Verify the file follows the format defined in `.claude/commands/chore.md`:
  - Metadata section with adw_id and prompt
  - Chore Description section with detailed explanation
  - Relevant Files section listing affected files
  - Step by Step Tasks section with numbered tasks
  - Validation Commands section with specific commands
  - Notes section (optional)
- Check that placeholders were properly replaced with actual values
- Verify the content is coherent and makes sense for the given prompt

### 6. Test Direct Manual Execution (Verification)
- Manually execute: `uv run /Users/ameno/dev/acidbath2/adws/adw_slash_command.py /chore "Manual test verification"`
- Verify the command executes without errors (exit code 0)
- Confirm console output shows success panel with green checkmark
- Check that output files are created in the expected `agents/<adw_id>/executor/` location
- Verify a new spec file is created in `specs/` directory
- Inspect the generated plan for proper formatting and content

### 7. Validate End-to-End Workflow Integration
- Ensure the complete workflow chain functions:
  1. `adw_slash_command.py` receives command and arguments
  2. Template is loaded from `.claude/commands/chore.md`
  3. Variables ($1, $2) are substituted with provided arguments
  4. Agent is executed via Claude Code CLI
  5. Output files are written to `agents/<adw_id>/<agent_name>/`
  6. Spec file is created in `specs/` directory
- Verify the workflow is fully observable through structured output
- Confirm error handling works for invalid inputs

### 8. Review Test Coverage and Improvements
- Document current test coverage: returncode check, directory existence
- Identify gaps: content validation, output structure validation, error scenarios
- Consider additional test cases: invalid arguments, missing templates, timeout scenarios
- Recommend improvements to the validation logic if needed

### 9. Run Full Validation Suite
- Execute: `uv run /Users/ameno/dev/acidbath2/adws/jerry_validate.py --level all`
- Verify that Level 3 validation passes along with all other levels
- Check for any warnings or failures in other validation levels
- Ensure the slash command test doesn't negatively impact other tests

## Validation Commands
Execute these commands to validate the chore is complete:

```bash
# 1. Validate Python syntax of core files
uv run python -m py_compile /Users/ameno/dev/acidbath2/adws/jerry_validate.py
uv run python -m py_compile /Users/ameno/dev/acidbath2/adws/adw_slash_command.py

# 2. Run Level 3 validation which includes slash command test
uv run /Users/ameno/dev/acidbath2/adws/jerry_validate.py --level 3

# 3. Verify the validation passed (exit code should be 0)
echo $?

# 4. Check that spec files were created
ls -la /Users/ameno/dev/acidbath2/specs/chore-*-jerry-validation-slash-command-test.md

# 5. Verify agent output directories exist
ls -la /Users/ameno/dev/acidbath2/agents/*/executor/

# 6. Inspect the summary output from most recent execution
cat /Users/ameno/dev/acidbath2/agents/*/executor/custom_summary_output.json | jq '.success, .slash_command, .args'

# 7. Test the script help flag
uv run /Users/ameno/dev/acidbath2/adws/adw_slash_command.py --help

# 8. Verify the chore template is readable
cat /Users/ameno/dev/acidbath2/.claude/commands/chore.md | head -20

# 9. Manual test execution
uv run /Users/ameno/dev/acidbath2/adws/adw_slash_command.py /chore "Manual verification test"

# 10. Run full validation suite to ensure nothing broke
uv run /Users/ameno/dev/acidbath2/adws/jerry_validate.py --level all --report /tmp/validation-report.json

# 11. Check validation report summary
cat /tmp/validation-report.json | jq '.summary'
```

## Notes

### Context
This chore is part of validating the export/import/bootstrap feature for Jerry (GitHub issue #18, adw_id: 53fe41e6). The validation system includes 5 levels:
- Level 1: Import validation (modules load correctly)
- Level 2: CLI validation (scripts executable, dependencies available)
- **Level 3: Workflow validation** (THIS CHORE - slash commands, worktree isolation)
- Level 4: Full SDLC validation (plan, build workflows)
- Level 5: Auth validation (GitHub/GitLab token auth)

### Why This Test Matters
This validation test is particularly important because:

1. **Level 3 Validation Critical**: The slash command test is part of Level 3 validation (Workflow Validation), which validates core Jerry workflows before testing full SDLC operations
2. **Template System Test**: It validates the entire template system including:
   - Template loading from `.claude/commands/`
   - Variable substitution ($1, $2, $ARGUMENTS)
   - Agent execution via Claude Code CLI
   - Output file generation
3. **Observable Output**: The test produces structured output that can be inspected to verify the workflow completed correctly
4. **Real-World Scenario**: The test simulates a realistic use case where a user would run a slash command with arguments
5. **Bootstrap Validation**: This test is executed during Jerry bootstrap to ensure the installation is functional

### Current Behavior
The Level 3 validation test (lines 418-446 in jerry_validate.py) executes:
```python
proc = subprocess.run(
    [str(script_path), "/chore", "Jerry validation slash command test"],
    cwd=base_path,
    capture_output=True,
    text=True,
    timeout=120
)
```

It validates:
- Script execution completes within 120 seconds
- Return code is 0 (success)
- specs/ directory exists
- Error output is captured if failure occurs

### Test Coverage Considerations
Current validation checks:
- ✓ Command execution (returncode == 0)
- ✓ Timeout handling (120s max)
- ✓ Directory existence (specs/)

Potential improvements:
- Content validation for generated spec file
- Validation of agent output structure
- Testing with different slash commands beyond `/chore`
- Error condition testing (invalid arguments, missing templates)
- Performance testing (execution time benchmarks)

### Expected Success Criteria
The validation script should report:
- "Slash command executed successfully" message
- Return code 0
- spec file created in `specs/` with pattern: `chore-<adw_id>-jerry-validation-slash-command-test.md`
- Agent output files created in `agents/<adw_id>/executor/`
- custom_summary_output.json contains: `"success": true`

### Dependencies
- Python 3.11+
- uv package manager (for script execution)
- Claude Code CLI (for agent execution)
- click>=8.0.0
- rich>=13.0.0
- pydantic
- python-dotenv
