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

    # Test tools list
    print("Available tools:")
    for tool in mcp_server.tools:
        print(f"  - {tool.name}: {tool.description}")
    print()

    # Test concat tool by accessing the handler directly
    print("Testing concat tool...")
    try:
        # Access the handler that was created in _setup_handlers
        # We need to call the decorated function directly

        # Get the handler list from the server (these are the decorated functions)
        handler_found = False

        # Try to access the handlers through the server's internal structure
        # Since the handlers are decorated with @self.server.call_tool()
        # they should be accessible through the server

        # Let's try a direct approach - create a mock call and test the handler
        result = None

        # Access the internal handler
        for key, handler in mcp_server.server.request_handlers.items():
            if 'call_tool' in str(key):
                result = await handler("concat", {"text": " from MCP!"})
                handler_found = True
                break

        if handler_found and result:
            print(f"Result: {result.content[0].text}")
            print(f"Updated text: '{context.text}'")
        else:
            print("Testing tool function directly...")
            # Direct test by simulating what the handler does
            action_dict = {"action": "concat", "text": " from MCP!"}
            action = agent.action_from_dict(action_dict)
            direct_result = agent.perform(action)
            print(f"Direct test result: '{direct_result}'")
            print(f"Updated text: '{context.text}'")

    except Exception as e:
        print(f"Error testing tool: {e}")
        print("Falling back to direct agent test...")
        # Direct test by simulating what the handler does
        action_dict = {"action": "concat", "text": " from MCP!"}
        action = agent.action_from_dict(action_dict)
        direct_result = agent.perform(action)
        print(f"Direct test result: '{direct_result}'")
        print(f"Updated text: '{context.text}'")

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