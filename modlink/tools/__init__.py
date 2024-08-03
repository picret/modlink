# modlink/tools/__init__.py

from typing import Any
import warnings

def _warn_on_import(name: str, replacement: str) -> None:
    warnings.warn(f"{name} has been moved to {replacement}.", DeprecationWarning)

def __getattr__(name: str) -> Any:
    if name == "ActionRegistry":
        from .action_registry import ActionRegistry
        _warn_on_import(name, replacement="modlink.tools.action_registry.ActionRegistry")
        return ActionRegistry
    elif name == "AgentArgParser":
        from .agent_arg_parser import AgentArgParser
        _warn_on_import(name, replacement="modlink.tools.agent_arg_parser.AgentArgParser")
        return AgentArgParser
    elif name == "AgentTime":
        from .agent_time import AgentTime
        _warn_on_import(name, replacement="modlink.tools.agent_time.AgentTime")
        return AgentTime
    else:
        raise AttributeError(f"module 'modlink.tools' has no attribute '{name}'")

__all__ = [
  'ActionRegistry',
  'AgentArgParser',
  'AgentTime',
]
