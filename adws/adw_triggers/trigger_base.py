#!/usr/bin/env python3
"""
Generic Trigger Infrastructure for Jerry

This module provides the base classes and registry for all triggers.
Triggers are pluggable - no hardcoded implementations here.

Usage:
    from adw_triggers import TriggerBase, TriggerEvent, TriggerRegistry

    class MyTrigger(TriggerBase):
        async def start(self) -> None: ...
        async def stop(self) -> None: ...
        async def on_event(self, event: TriggerEvent) -> None: ...

    TriggerRegistry.register("my_trigger", MyTrigger)
"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, Any, Type, Optional, List, Callable, Awaitable
from pydantic import BaseModel, Field


class TriggerEvent(BaseModel):
    """Generic trigger event - source-agnostic."""

    event_type: str = Field(
        description="Type of event (e.g., 'issue_created', 'comment_added', 'cron_tick')"
    )
    payload: Dict[str, Any] = Field(
        default_factory=dict,
        description="Event-specific payload data"
    )
    source: str = Field(
        description="Source of the event (e.g., 'github_webhook', 'cron', 'manual')"
    )
    timestamp: datetime = Field(
        default_factory=datetime.now,
        description="When the event occurred"
    )

    # Optional metadata
    adw_id: Optional[str] = Field(
        default=None,
        description="ADW ID if this event is part of an existing workflow"
    )
    issue_number: Optional[int] = Field(
        default=None,
        description="GitHub issue number if applicable"
    )
    repo_path: Optional[str] = Field(
        default=None,
        description="Repository path (owner/repo) if applicable"
    )


class TriggerResult(BaseModel):
    """Result of processing a trigger event."""

    success: bool
    adw_id: Optional[str] = None
    workflow: Optional[str] = None
    message: Optional[str] = None
    error: Optional[str] = None


EventHandler = Callable[[TriggerEvent], Awaitable[TriggerResult]]


class TriggerBase(ABC):
    """Abstract base class for all triggers."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.handlers: List[EventHandler] = []
        self._running = False

    def add_handler(self, handler: EventHandler) -> None:
        """Add an event handler."""
        self.handlers.append(handler)

    def remove_handler(self, handler: EventHandler) -> None:
        """Remove an event handler."""
        if handler in self.handlers:
            self.handlers.remove(handler)

    async def dispatch(self, event: TriggerEvent) -> List[TriggerResult]:
        """Dispatch event to all registered handlers."""
        results = []
        for handler in self.handlers:
            try:
                result = await handler(event)
                results.append(result)
            except Exception as e:
                results.append(TriggerResult(
                    success=False,
                    error=str(e)
                ))
        return results

    @abstractmethod
    async def start(self) -> None:
        """Start the trigger (e.g., start listening for webhooks)."""
        pass

    @abstractmethod
    async def stop(self) -> None:
        """Stop the trigger gracefully."""
        pass

    @abstractmethod
    async def on_event(self, event: TriggerEvent) -> None:
        """Handle an incoming event."""
        pass

    @property
    def is_running(self) -> bool:
        """Check if trigger is currently running."""
        return self._running


class TriggerRegistry:
    """Registry for available triggers - no hardcoding."""

    _triggers: Dict[str, Type[TriggerBase]] = {}
    _instances: Dict[str, TriggerBase] = {}

    @classmethod
    def register(cls, name: str, trigger_class: Type[TriggerBase]) -> None:
        """Register a trigger type."""
        cls._triggers[name] = trigger_class

    @classmethod
    def get(cls, name: str) -> Optional[Type[TriggerBase]]:
        """Get a trigger class by name."""
        return cls._triggers.get(name)

    @classmethod
    def create(
        cls,
        name: str,
        config: Optional[Dict[str, Any]] = None
    ) -> Optional[TriggerBase]:
        """Create a trigger instance."""
        trigger_class = cls.get(name)
        if trigger_class:
            instance = trigger_class(config)
            cls._instances[name] = instance
            return instance
        return None

    @classmethod
    def get_instance(cls, name: str) -> Optional[TriggerBase]:
        """Get an existing trigger instance."""
        return cls._instances.get(name)

    @classmethod
    def list_triggers(cls) -> List[str]:
        """List all registered trigger names."""
        return list(cls._triggers.keys())

    @classmethod
    def list_running(cls) -> List[str]:
        """List all running trigger instances."""
        return [name for name, inst in cls._instances.items() if inst.is_running]
