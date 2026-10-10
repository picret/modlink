#!/usr/bin/env python3
"""
Example MCP Server using modlink

This demonstrates how to expose modlink agent actions as MCP tools.
Run with: python example/mcp_server.py
"""

import asyncio
import logging
from modlink.tools import AgentMCPServer
from example.agent import ExampleAgent
from example.context import ExampleContext


async def main():
    """Run the example MCP server."""
    # Setup logging
    logging.basicConfig(level=logging.INFO)

    # Create and setup the agent
    agent = ExampleAgent()
    context = ExampleContext()
    agent.attach(context)

    # Create MCP server
    mcp_server = AgentMCPServer(agent, "example-mcp-server")

    logging.info(f"Starting MCP server: {mcp_server.server_name}")
    logging.info(f"Available tools: {[tool.name for tool in mcp_server.tools]}")

    try:
        # Run the MCP server
        await mcp_server.run_stdio()
    finally:
        # Clean up
        agent.detach()


if __name__ == "__main__":
    asyncio.run(main())