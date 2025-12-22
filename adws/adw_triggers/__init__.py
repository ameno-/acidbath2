"""
ADW Triggers - Pluggable trigger infrastructure for Jerry

This module provides a generic trigger framework that can be extended
with various trigger implementations (webhooks, cron, manual, etc.).
"""

from .trigger_base import TriggerBase, TriggerEvent, TriggerRegistry

__all__ = ["TriggerBase", "TriggerEvent", "TriggerRegistry"]
