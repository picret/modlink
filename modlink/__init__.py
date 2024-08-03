# modlink/__init__.py

# Do not manually edit here. This is updated by scripts/prepare_release.py.
__version__ = "0.1.0a1"


import warnings
from typing import Any


def _warn_on_import(name: str, replacement: str) -> None:
    warnings.warn(f"{name} has been moved to {replacement}.", DeprecationWarning)


def __getattr__(name: str) -> Any:
    if name == "Agent":
        from .agent import Agent
        _warn_on_import(name, replacement="modlink.agent.Agent")
        return Agent
    elif name == "agent_name":
        from .agent import agent_name
        _warn_on_import(name, replacement="modlink.agent.agent_name")
        return agent_name
    elif name == "Action":
        from .action import Action
        _warn_on_import(name, replacement="modlink.action.Action")
        return Action
    elif name == "action_name":
        from .action import action_name
        _warn_on_import(name, replacement="modlink.action.action_name")
        return action_name
    elif name == "Context":
        from .context import Context
        _warn_on_import(name, replacement="modlink.context.Context")
        return Context
    elif name == "Platform":
        from .platform import Platform
        _warn_on_import(name, replacement="modlink.platform.Platform")
        return Platform
    else:
        raise AttributeError(f"module 'modlink' has no attribute '{name}'")


__all__ = [
  'Agent', 'agent_name',
  'Action', 'action_name',
  'Context',
  'Platform',
]