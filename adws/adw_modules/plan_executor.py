"""Plan executor module for multi-step orchestration.

Parses spec files into structured ExecutionPlans and provides
utilities for step-level execution with parallel support.

Key classes:
- PlanParser: Parse spec content into ExecutionPlan with groups/steps
- StepExecutor: Execute individual steps (Step 6)
- MultiPhaseOrchestrator: Coordinate group execution (Step 6)
"""

import re
import logging
from typing import Optional, Tuple, List
from pathlib import Path

from .data_types import (
    ExecutionPlan,
    StepGroup,
    StepDefinition,
    StepStatus,
    ModelStrategy,
)


class PlanParser:
    """Parse spec markdown into structured ExecutionPlan.

    Parses the new group format:
        ### Group A: Title [parallel: true, depends: B, model: opus]
        #### Step A.1: Step Title
        - bullet points

    Falls back to legacy format (### 1. Title) as single sequential group.
    """

    # Pattern for new group format: ### Group X: Title [options]
    GROUP_PATTERN = re.compile(
        r"^###\s+Group\s+([A-Z]):\s+(.+?)\s*\[([^\]]*)\]\s*$", re.MULTILINE
    )

    # Pattern for step format: #### Step X.N: Title
    STEP_PATTERN = re.compile(
        r"^####\s+Step\s+([A-Z])\.(\d+):\s+(.+)$", re.MULTILINE
    )

    # Pattern for legacy format: ### N. Title
    LEGACY_STEP_PATTERN = re.compile(r"^###\s+(\d+)\.\s+(.+)$", re.MULTILINE)

    def __init__(self, logger: Optional[logging.Logger] = None):
        self.logger = logger or logging.getLogger(__name__)

    def parse(self, content: str, plan_file: str) -> ExecutionPlan:
        """Parse spec content into ExecutionPlan.

        Args:
            content: Markdown content of the spec file
            plan_file: Path to the spec file (for reference)

        Returns:
            ExecutionPlan with groups and steps extracted
        """
        # Try new group format first
        groups = self._parse_groups(content)

        if groups:
            self.logger.info(
                f"Parsed {len(groups)} groups with new format from {plan_file}"
            )
            return ExecutionPlan(plan_file=plan_file, groups=groups)

        # Fall back to legacy format
        legacy_groups = self._parse_legacy_format(content)
        if legacy_groups:
            self.logger.info(
                f"Parsed {len(legacy_groups)} steps with legacy format from {plan_file}"
            )
            return ExecutionPlan(plan_file=plan_file, groups=legacy_groups)

        # No steps found
        self.logger.warning(f"No steps found in {plan_file}")
        return ExecutionPlan(plan_file=plan_file, groups=[])

    def _parse_groups(self, content: str) -> List[StepGroup]:
        """Parse new group format from content."""
        groups: List[StepGroup] = []

        # Find all group headers
        group_matches = list(self.GROUP_PATTERN.finditer(content))
        if not group_matches:
            return []

        for i, match in enumerate(group_matches):
            group_id = match.group(1)
            title = match.group(2).strip()
            options_str = match.group(3)

            # Parse options
            parallel, depends_on, model_strategy = self._parse_group_options(
                options_str
            )

            # Find content between this group and next (or end)
            start_pos = match.end()
            end_pos = (
                group_matches[i + 1].start()
                if i + 1 < len(group_matches)
                else len(content)
            )
            group_content = content[start_pos:end_pos]

            # Parse steps in this group
            steps = self._parse_steps(group_content, group_id)

            group = StepGroup(
                group_id=group_id,
                title=title,
                parallel=parallel,
                depends_on=depends_on,
                model_strategy=model_strategy,
                steps=steps,
            )
            groups.append(group)

        return groups

    def _parse_group_options(
        self, options_str: str
    ) -> Tuple[bool, List[str], ModelStrategy]:
        """Parse group options from bracket content.

        Example: "parallel: true, depends: A, B, model: opus"
        """
        parallel = False
        depends_on: List[str] = []
        model_strategy: ModelStrategy = "auto"

        # Parse parallel
        parallel_match = re.search(r"parallel:\s*(true|false)", options_str, re.I)
        if parallel_match:
            parallel = parallel_match.group(1).lower() == "true"

        # Parse depends
        depends_match = re.search(r"depends:\s*([A-Z](?:\s*,\s*[A-Z])*)", options_str)
        if depends_match:
            depends_str = depends_match.group(1)
            depends_on = [d.strip() for d in depends_str.split(",")]

        # Parse model
        model_match = re.search(r"model:\s*(auto|sonnet|opus|heavy-for-build)", options_str, re.I)
        if model_match:
            model_strategy = model_match.group(1).lower()  # type: ignore

        return parallel, depends_on, model_strategy

    def _parse_steps(self, content: str, group_id: str) -> List[StepDefinition]:
        """Parse steps from group content."""
        steps: List[StepDefinition] = []

        # Find all step headers
        step_matches = list(self.STEP_PATTERN.finditer(content))

        for i, match in enumerate(step_matches):
            step_group = match.group(1)
            step_num = match.group(2)
            title = match.group(3).strip()

            # Verify step belongs to this group
            if step_group != group_id:
                self.logger.warning(
                    f"Step {step_group}.{step_num} found in group {group_id}, skipping"
                )
                continue

            step_id = f"{group_id}.{step_num}"

            # Find content between this step and next (or end)
            start_pos = match.end()
            end_pos = (
                step_matches[i + 1].start()
                if i + 1 < len(step_matches)
                else len(content)
            )
            description = content[start_pos:end_pos].strip()

            # Clean up description (remove trailing group headers if any)
            if "### Group" in description:
                description = description[: description.index("### Group")].strip()

            step = StepDefinition(
                step_id=step_id,
                group_id=group_id,
                title=title,
                description=description,
                status=StepStatus.PENDING,
            )
            steps.append(step)

        return steps

    def _parse_legacy_format(self, content: str) -> List[StepGroup]:
        """Parse legacy step format (### 1. Title) as single sequential group."""
        steps: List[StepDefinition] = []

        step_matches = list(self.LEGACY_STEP_PATTERN.finditer(content))
        if not step_matches:
            return []

        for i, match in enumerate(step_matches):
            step_num = match.group(1)
            title = match.group(2).strip()
            step_id = f"A.{step_num}"

            # Find content between this step and next (or end)
            start_pos = match.end()
            end_pos = (
                step_matches[i + 1].start()
                if i + 1 < len(step_matches)
                else len(content)
            )
            description = content[start_pos:end_pos].strip()

            # Clean up description (remove validation/notes sections)
            for section in ["## Validation", "## Notes", "## Testing", "## Acceptance"]:
                if section in description:
                    description = description[: description.index(section)].strip()

            step = StepDefinition(
                step_id=step_id,
                group_id="A",
                title=title,
                description=description,
                status=StepStatus.PENDING,
            )
            steps.append(step)

        # Wrap in single sequential group
        return [
            StepGroup(
                group_id="A",
                title="Implementation",
                parallel=False,
                depends_on=[],
                model_strategy="auto",
                steps=steps,
            )
        ]

    def parse_file(self, plan_path: str) -> ExecutionPlan:
        """Convenience method to parse from file path."""
        path = Path(plan_path)
        if not path.exists():
            raise FileNotFoundError(f"Plan file not found: {plan_path}")
        content = path.read_text()
        return self.parse(content, plan_path)


from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import os

from .agent import execute_template, prompt_claude_code_with_retry
from .data_types import (
    AgentPromptRequest,
    AgentPromptResponse,
    AgentTemplateRequest,
    RetryCode,
)


@dataclass
class StepResult:
    """Result of executing a single step."""

    step_id: str
    success: bool
    output: str
    commit_hash: Optional[str] = None
    error_message: Optional[str] = None


@dataclass
class GroupResult:
    """Result of executing a group of steps."""

    group_id: str
    success: bool
    step_results: List[StepResult]
    error_message: Optional[str] = None


@dataclass
class PlanResult:
    """Result of executing an entire plan."""

    success: bool
    plan_file: str
    group_results: List[GroupResult]
    completed_steps: int
    total_steps: int
    error_message: Optional[str] = None


class StepExecutor:
    """Execute individual steps with model selection.

    Uses the /implement_step slash command to execute focused steps,
    or falls back to direct prompts for simple steps.
    """

    def __init__(
        self,
        adw_id: str,
        working_dir: str,
        logger: Optional[logging.Logger] = None,
    ):
        self.adw_id = adw_id
        self.working_dir = working_dir
        self.logger = logger or logging.getLogger(__name__)

    def execute_step(
        self,
        step: StepDefinition,
        group: StepGroup,
        use_slash_command: bool = True,
    ) -> StepResult:
        """Execute a single step.

        Args:
            step: The step to execute
            group: The group this step belongs to (for model selection)
            use_slash_command: Whether to use /implement_step (True) or direct prompt

        Returns:
            StepResult with success status and output
        """
        self.logger.info(f"Executing Step {step.step_id}: {step.title}")

        # Select model based on group strategy
        model = self._select_model(step, group)
        self.logger.info(f"Using model: {model}")

        # Mark step as in progress
        step.status = StepStatus.IN_PROGRESS
        step.adw_id = self.adw_id

        try:
            if use_slash_command:
                response = self._execute_with_slash_command(step, model)
            else:
                response = self._execute_with_direct_prompt(step, model)

            if response.success:
                step.status = StepStatus.COMPLETED
                step.result_summary = response.output[:500]  # Truncate for storage
                return StepResult(
                    step_id=step.step_id,
                    success=True,
                    output=response.output,
                )
            else:
                step.status = StepStatus.FAILED
                step.error_message = response.output[:500]
                return StepResult(
                    step_id=step.step_id,
                    success=False,
                    output=response.output,
                    error_message=response.output,
                )

        except Exception as e:
            error_msg = str(e)
            self.logger.error(f"Step {step.step_id} failed with exception: {error_msg}")
            step.status = StepStatus.FAILED
            step.error_message = error_msg
            return StepResult(
                step_id=step.step_id,
                success=False,
                output="",
                error_message=error_msg,
            )

    def _select_model(self, step: StepDefinition, group: StepGroup) -> str:
        """Select model based on group strategy.

        Args:
            step: The step being executed
            group: The group containing the step

        Returns:
            "sonnet" or "opus"
        """
        strategy = group.model_strategy

        if strategy == "opus":
            return "opus"
        elif strategy == "sonnet":
            return "sonnet"
        elif strategy == "heavy-for-build":
            # Use opus for implementation steps
            title_lower = step.title.lower()
            if any(
                keyword in title_lower
                for keyword in ["implement", "create", "build", "write", "add"]
            ):
                return "opus"
            return "sonnet"
        else:  # "auto"
            # Estimate complexity based on description length
            if len(step.description) > 1000:
                return "opus"
            return "sonnet"

    def _execute_with_slash_command(
        self, step: StepDefinition, model: str
    ) -> AgentPromptResponse:
        """Execute step using /implement_step slash command."""
        request = AgentTemplateRequest(
            agent_name=f"step-{step.step_id.replace('.', '-')}",
            slash_command="/implement_step",
            args=[step.step_id, step.title, step.description],
            adw_id=self.adw_id,
            model=model,
            working_dir=self.working_dir,
        )
        return execute_template(request)

    def _execute_with_direct_prompt(
        self, step: StepDefinition, model: str
    ) -> AgentPromptResponse:
        """Execute step using direct prompt."""
        prompt = f"""Execute Step {step.step_id}: {step.title}

## Instructions
{step.description}

## Requirements
- Read relevant files BEFORE making changes
- Execute ALL bullet points in the instructions
- Validate changes compile after implementation
- Do NOT commit - just implement and validate

## Report
After completing, summarize:
- Files modified
- Key changes made
- Validation results
"""
        # Create output directory
        output_dir = os.path.join(
            self.working_dir or ".",
            "agents",
            self.adw_id,
            f"step-{step.step_id.replace('.', '-')}",
        )
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, "cc_raw_output.jsonl")

        request = AgentPromptRequest(
            prompt=prompt,
            adw_id=self.adw_id,
            agent_name=f"step-{step.step_id.replace('.', '-')}",
            model=model,
            dangerously_skip_permissions=True,
            output_file=output_file,
            working_dir=self.working_dir,
        )
        return prompt_claude_code_with_retry(request)


class MultiPhaseOrchestrator:
    """Coordinate multi-phase workflow execution.

    Pattern from legacy adw_plan_implement_update_task.py:
    - Separate agent per phase for context isolation
    - Phase gating (only proceed if previous phase succeeded)
    - State tracking between phases
    - Per-phase summaries for observability
    - Parallel execution within groups via ThreadPoolExecutor
    """

    def __init__(
        self,
        adw_id: str,
        working_dir: str,
        logger: Optional[logging.Logger] = None,
        max_workers: int = 3,
    ):
        self.adw_id = adw_id
        self.working_dir = working_dir
        self.logger = logger or logging.getLogger(__name__)
        self.max_workers = max_workers
        self.step_executor = StepExecutor(adw_id, working_dir, logger)

    def execute_plan(self, plan: ExecutionPlan) -> PlanResult:
        """Execute an entire plan with group-level orchestration.

        Args:
            plan: The parsed ExecutionPlan to execute

        Returns:
            PlanResult with all group and step results
        """
        self.logger.info(
            f"Starting plan execution: {plan.plan_file} "
            f"({len(plan.groups)} groups, {plan.total_steps()} steps)"
        )

        group_results: List[GroupResult] = []
        completed_groups: set = set()
        failed = False

        # Execute groups in dependency order
        while True:
            eligible = self._get_eligible_groups(plan, completed_groups)

            if not eligible:
                # No more groups to execute
                break

            for group in eligible:
                if failed and not self._can_skip_on_failure(group, plan):
                    # Skip dependent groups if a dependency failed
                    self.logger.warning(
                        f"Skipping Group {group.group_id} due to dependency failure"
                    )
                    group_result = GroupResult(
                        group_id=group.group_id,
                        success=False,
                        step_results=[],
                        error_message="Skipped due to dependency failure",
                    )
                    group_results.append(group_result)
                    completed_groups.add(group.group_id)
                    continue

                self.logger.info(
                    f"Starting Group {group.group_id}: {group.title} "
                    f"({len(group.steps)} steps, parallel={group.parallel})"
                )

                group_result = self._execute_group(group)
                group_results.append(group_result)
                completed_groups.add(group.group_id)

                if not group_result.success:
                    failed = True
                    self.logger.error(
                        f"Group {group.group_id} failed: {group_result.error_message}"
                    )

        # Calculate totals
        completed_steps = sum(
            1
            for gr in group_results
            for sr in gr.step_results
            if sr.success
        )

        return PlanResult(
            success=not failed,
            plan_file=plan.plan_file,
            group_results=group_results,
            completed_steps=completed_steps,
            total_steps=plan.total_steps(),
            error_message="One or more groups failed" if failed else None,
        )

    def _get_eligible_groups(
        self, plan: ExecutionPlan, completed_groups: set
    ) -> List[StepGroup]:
        """Get groups whose dependencies are satisfied and not yet completed."""
        eligible = []
        for group in plan.groups:
            if group.group_id in completed_groups:
                continue
            if all(dep in completed_groups for dep in group.depends_on):
                eligible.append(group)
        return eligible

    def _can_skip_on_failure(self, group: StepGroup, plan: ExecutionPlan) -> bool:
        """Check if a group can be skipped when a dependency fails.

        Groups with no dependencies can always run.
        """
        return len(group.depends_on) == 0

    def _execute_group(self, group: StepGroup) -> GroupResult:
        """Execute all steps in a group.

        Uses parallel execution if group.parallel is True.
        """
        if not group.steps:
            return GroupResult(
                group_id=group.group_id,
                success=True,
                step_results=[],
            )

        if group.parallel and len(group.steps) > 1:
            return self._execute_parallel_steps(group)
        else:
            return self._execute_sequential_steps(group)

    def _execute_sequential_steps(self, group: StepGroup) -> GroupResult:
        """Execute steps sequentially, stopping on failure."""
        step_results: List[StepResult] = []
        failed = False

        for step in group.steps:
            if failed:
                # Mark remaining steps as skipped
                step.status = StepStatus.SKIPPED
                step_results.append(
                    StepResult(
                        step_id=step.step_id,
                        success=False,
                        output="",
                        error_message="Skipped due to earlier failure",
                    )
                )
                continue

            result = self.step_executor.execute_step(step, group)
            step_results.append(result)

            if not result.success:
                failed = True
                self.logger.error(f"Step {step.step_id} failed: {result.error_message}")

        return GroupResult(
            group_id=group.group_id,
            success=not failed,
            step_results=step_results,
            error_message="One or more steps failed" if failed else None,
        )

    def _execute_parallel_steps(self, group: StepGroup) -> GroupResult:
        """Execute steps in parallel using ThreadPoolExecutor."""
        step_results: List[StepResult] = []
        failed = False

        self.logger.info(
            f"Executing {len(group.steps)} steps in parallel "
            f"(max_workers={self.max_workers})"
        )

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all steps
            future_to_step = {
                executor.submit(
                    self.step_executor.execute_step, step, group
                ): step
                for step in group.steps
            }

            # Collect results as they complete
            for future in as_completed(future_to_step):
                step = future_to_step[future]
                try:
                    result = future.result()
                    step_results.append(result)
                    if not result.success:
                        failed = True
                        self.logger.error(
                            f"Step {step.step_id} failed: {result.error_message}"
                        )
                except Exception as e:
                    failed = True
                    error_msg = str(e)
                    self.logger.error(
                        f"Step {step.step_id} raised exception: {error_msg}"
                    )
                    step_results.append(
                        StepResult(
                            step_id=step.step_id,
                            success=False,
                            output="",
                            error_message=error_msg,
                        )
                    )

        return GroupResult(
            group_id=group.group_id,
            success=not failed,
            step_results=step_results,
            error_message="One or more steps failed" if failed else None,
        )

    def execute_plan_file(self, plan_path: str) -> PlanResult:
        """Convenience method to parse and execute a plan file."""
        parser = PlanParser(self.logger)
        plan = parser.parse_file(plan_path)
        return self.execute_plan(plan)
