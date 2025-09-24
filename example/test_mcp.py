#!/usr/bin/env python3
"""
Test script for MCP server functionality
"""

import asyncio
from modlink.tools import AgentMCPServer
from example.agent import ExampleAgent
from example.context import ExampleContext


async def test_mcp_tools():
    """Test MCP tool execution."""
    # Setup agent
    agent = ExampleAgent()
    context = ExampleContext()
    context.text = "Hello World"  # Initial text
    agent.attach(context)

    # Create MCP server
    mcp_server = AgentMCPServer(agent)

    print(f"Initial text: '{context.text}'")
    print()

    # Test concat tool
    print("Testing concat tool...")
    try:
        result = await mcp_server._setup_handlers.__wrapped__(mcp_server)  # Access handlers
        # Simulate tool call
        from mcp.types import CallToolResult

        # Get the actual handler
        handler = None
        for handler_func in mcp_server.server._request_handlers.values():
            if hasattr(handler_func, '__name__') and 'call_tool' in str(handler_func):
                handler = handler_func
                break

        if handler:
            result = await handler("concat", {"text": " from MCP!"})
            print(f"Result: {result.content[0].text}")
            print(f"Updated text: '{context.text}'")
        else:
            print("Could not find call_tool handler")

    except Exception as e:
        print(f"Error: {e}")

    # Clean up
    agent.detach()


async def simple_test():
    """Simple test by directly calling agent methods."""
    # Setup agent
    agent = ExampleAgent()
    context = ExampleContext()
    context.text = "Hello World"
    agent.attach(context)

    print(f"Initial text: '{context.text}'")

    # Test action execution directly
    action = agent.action_from_dict({"action": "concat", "text": " from MCP!"})
    result = agent.perform(action)

    print(f"Action result: '{result}'")
    print(f"Updated text: '{context.text}'")

    # Test another action
    action = agent.action_from_dict({"action": "case", "operation": "upper"})
    result = agent.perform(action)

    print(f"After uppercase: '{result}'")

    agent.detach()


if __name__ == "__main__":
    print("=== Simple Test ===")
    asyncio.run(simple_test())
    print()
    print("=== MCP Test ===")
    asyncio.run(test_mcp_tools())