#!/usr/bin/env python3
"""
Manual Trigger for Jerry

Always included in Jerry core - allows programmatic triggering of ADW workflows
without external event sources.

Usage:
    from adw_triggers.trigger_manual import ManualTrigger

    trigger = ManualTrigger()
    await trigger.emit_issue_event(issue_number=123, workflow="adw_plan_iso")
"""

import sys
import os
from datetime import datetime
from typing import Dict, Any, Optional, List

# Add project root for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from adws.adw_triggers.trigger_base import (
    TriggerBase,
    TriggerEvent,
    TriggerResult,
    TriggerRegistry,
)


class ManualTrigger(TriggerBase):
    """Manual trigger for programmatic workflow invocation."""

    async def start(self) -> None:
        """Manual trigger is always ready."""
        self._running = True

    async def stop(self) -> None:
        """Stop the manual trigger."""
        self._running = False

    async def on_event(self, event: TriggerEvent) -> None:
        """Process a manually triggered event."""
        await self.dispatch(event)

    async def emit(
        self,
        event_type: str,
        payload: Optional[Dict[str, Any]] = None,
        issue_number: Optional[int] = None,
        adw_id: Optional[str] = None,
        repo_path: Optional[str] = None,
    ) -> List[TriggerResult]:
        """Emit a manual event."""
        event = TriggerEvent(
            event_type=event_type,
            payload=payload or {},
            source="manual",
            timestamp=datetime.now(),
            issue_number=issue_number,
            adw_id=adw_id,
            repo_path=repo_path,
        )
        return await self.dispatch(event)

    async def emit_issue_event(
        self,
        issue_number: int,
        workflow: str,
        repo_path: Optional[str] = None,
        adw_id: Optional[str] = None,
    ) -> List[TriggerResult]:
        """Emit an event to trigger a workflow for a GitHub issue."""
        return await self.emit(
            event_type="issue_workflow",
            payload={"workflow": workflow},
            issue_number=issue_number,
            repo_path=repo_path,
            adw_id=adw_id,
        )

    async def emit_plan_event(
        self,
        issue_number: int,
        repo_path: Optional[str] = None,
    ) -> List[TriggerResult]:
        """Emit a plan workflow trigger."""
        return await self.emit_issue_event(
            issue_number=issue_number,
            workflow="adw_plan_iso",
            repo_path=repo_path,
        )

    async def emit_build_event(
        self,
        issue_number: int,
        adw_id: str,
        repo_path: Optional[str] = None,
    ) -> List[TriggerResult]:
        """Emit a build workflow trigger (requires existing ADW ID)."""
        return await self.emit_issue_event(
            issue_number=issue_number,
            workflow="adw_build_iso",
            repo_path=repo_path,
            adw_id=adw_id,
        )

    async def emit_patch_event(
        self,
        issue_number: int,
        repo_path: Optional[str] = None,
    ) -> List[TriggerResult]:
        """Emit a patch workflow trigger."""
        return await self.emit_issue_event(
            issue_number=issue_number,
            workflow="adw_patch_iso",
            repo_path=repo_path,
        )


# Register with the registry
TriggerRegistry.register("manual", ManualTrigger)
