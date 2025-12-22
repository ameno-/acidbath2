#!/usr/bin/env -S uv run
# /// script
# dependencies = []
# ///

"""
MCP Operations Module

Dynamic MCP management for on-demand loading of MCP servers.
This allows ADWs to enable/disable MCPs as needed without affecting other workflows.

Usage:
    from adws.adw_modules.mcp_ops import enable_playwright_mcp, disable_playwright_mcp

    # Enable before review/e2e testing
    enable_playwright_mcp(worktree_path)

    # Disable after completion
    disable_playwright_mcp(worktree_path)
"""

import shutil
import logging
from pathlib import Path


def enable_playwright_mcp(worktree_path: str, logger: logging.Logger = None) -> bool:
    """
    Enable Playwright MCP for this session by copying template to .mcp.json.

    Args:
        worktree_path: Path to the worktree directory
        logger: Optional logger instance

    Returns:
        True if MCP was enabled, False if template not found or already enabled
    """
    template = Path(worktree_path) / ".mcp.playwright.json"
    target = Path(worktree_path) / ".mcp.json"

    if not template.exists():
        if logger:
            logger.warning(f"Playwright MCP template not found: {template}")
        return False

    if target.exists():
        if logger:
            logger.info("MCP already enabled, skipping")
        return True

    try:
        shutil.copy(template, target)
        if logger:
            logger.info(f"Enabled Playwright MCP: {target}")
        return True
    except Exception as e:
        if logger:
            logger.error(f"Failed to enable Playwright MCP: {e}")
        return False


def disable_playwright_mcp(worktree_path: str, logger: logging.Logger = None) -> bool:
    """
    Disable Playwright MCP after review by removing .mcp.json.

    Args:
        worktree_path: Path to the worktree directory
        logger: Optional logger instance

    Returns:
        True if MCP was disabled, False if not found
    """
    target = Path(worktree_path) / ".mcp.json"

    if not target.exists():
        if logger:
            logger.debug("No MCP to disable")
        return True

    try:
        target.unlink()
        if logger:
            logger.info(f"Disabled Playwright MCP: {target}")
        return True
    except Exception as e:
        if logger:
            logger.error(f"Failed to disable Playwright MCP: {e}")
        return False


def is_playwright_mcp_enabled(worktree_path: str) -> bool:
    """
    Check if Playwright MCP is currently enabled.

    Args:
        worktree_path: Path to the worktree directory

    Returns:
        True if .mcp.json exists
    """
    target = Path(worktree_path) / ".mcp.json"
    return target.exists()


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print("Usage: mcp_ops.py <enable|disable|status> <worktree_path>")
        sys.exit(1)

    action = sys.argv[1]
    worktree_path = sys.argv[2]

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("mcp_ops")

    if action == "enable":
        success = enable_playwright_mcp(worktree_path, logger)
        sys.exit(0 if success else 1)
    elif action == "disable":
        success = disable_playwright_mcp(worktree_path, logger)
        sys.exit(0 if success else 1)
    elif action == "status":
        enabled = is_playwright_mcp_enabled(worktree_path)
        print(f"Playwright MCP: {'enabled' if enabled else 'disabled'}")
        sys.exit(0)
    else:
        print(f"Unknown action: {action}")
        sys.exit(1)
