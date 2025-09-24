import asyncio
import json
import sys
from typing import Any, Dict, List, Optional, Sequence

import anyio
from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.types import (
    Tool,
    TextContent,
    CallToolRequest,
    CallToolResult,
    ListToolsRequest,
)

from modlink import Agent


class AgentMCPServer:
    """
    MCP Server that exposes modlink agent actions as MCP tools.
    """

    def __init__(self, agent: Agent, server_name: Optional[str] = None):
        self.agent = agent
        self.server_name = server_name or f"{agent.name()}-mcp-server"
        self.server = Server(self.server_name)
        self.tools = self._build_tools()
        self._setup_handlers()

    def _build_tools(self) -> List[Tool]:
        """
        Convert agent action schemas to MCP tools.
        Similar to how AgentArgParser builds argument parsers.
        """
        tools = []
        schemas = self.agent.schemas()

        for schema in schemas:
            action_name = schema["properties"]["action"]["value"]
            description = schema.get("description", "")

            # Convert pydantic schema to MCP inputSchema
            input_schema = self._convert_to_mcp_schema(schema)

            tool = Tool(
                name=action_name,
                description=description,
                inputSchema=input_schema
            )
            tools.append(tool)

        return tools

    def _convert_to_mcp_schema(self, pydantic_schema: Dict) -> Dict:
        """
        Convert a pydantic schema to MCP tool inputSchema format.
        """
        properties = {}
        required = []

        # Extract properties, excluding the 'action' field
        for prop_name, prop_details in pydantic_schema.get("properties", {}).items():
            if prop_name == "action":
                continue  # Skip action field as it's handled by tool name

            properties[prop_name] = self._convert_property(prop_details, pydantic_schema.get("$defs", {}))

            # Check if required
            if prop_name in pydantic_schema.get("required", []):
                required.append(prop_name)

        input_schema = {
            "type": "object",
            "properties": properties,
        }

        if required:
            input_schema["required"] = required

        return input_schema

    def _convert_property(self, prop_details: Dict, definitions: Dict) -> Dict:
        """
        Convert a single property from pydantic schema to MCP format.
        """
        if "type" in prop_details:
            # Simple type
            return {
                "type": prop_details["type"],
                "description": prop_details.get("description", "")
            }
        elif "$ref" in prop_details:
            # Reference to enum or other definition
            ref_key = prop_details["$ref"].split("/")[-1]
            if ref_key in definitions:
                ref_def = definitions[ref_key]
                if "enum" in ref_def:
                    return {
                        "type": ref_def.get("type", "string"),
                        "enum": ref_def["enum"],
                        "description": prop_details.get("description", "")
                    }
        elif "anyOf" in prop_details or "oneOf" in prop_details:
            # Handle Optional and Union types
            sub_schemas = prop_details.get("anyOf") or prop_details.get("oneOf")
            # Find the non-null type
            for sub_schema in sub_schemas:
                if sub_schema.get("type") != "null":
                    return self._convert_property(sub_schema, definitions)
        elif "allOf" in prop_details:
            # Handle references in allOf
            ref = prop_details["allOf"][0].get("$ref")
            if ref:
                return self._convert_property({"$ref": ref}, definitions)

        # Fallback to string type
        return {
            "type": "string",
            "description": prop_details.get("description", "")
        }

    def _setup_handlers(self):
        """Set up MCP request handlers."""

        @self.server.list_tools()
        async def handle_list_tools() -> List[Tool]:
            return self.tools

        @self.server.call_tool()
        async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> CallToolResult:
            """Handle tool calls by delegating to agent actions."""
            try:
                # Create action from tool call
                action_dict = {"action": name, **arguments}
                action = self.agent.action_from_dict(action_dict)

                # Perform action
                result = self.agent.perform(action)

                # Format result as text
                result_text = self._format_result(result)

                return CallToolResult(
                    content=[TextContent(type="text", text=result_text)],
                    isError=False
                )

            except Exception as e:
                error_msg = f"Error executing tool '{name}': {str(e)}"
                return CallToolResult(
                    content=[TextContent(type="text", text=error_msg)],
                    isError=True
                )

    def _format_result(self, result: Any) -> str:
        """Format the action result as a string for MCP response."""
        if isinstance(result, str):
            return result
        elif result is None:
            return "Action completed successfully"
        else:
            try:
                return json.dumps(result, indent=2, default=str)
            except (TypeError, ValueError):
                return str(result)

    async def run_stdio(self):
        """Run the MCP server using stdio transport."""
        from mcp.server.stdio import stdio_server

        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name=self.server_name,
                    server_version="1.0.0",
                    capabilities={}
                )
            )

    async def run(self, read_stream, write_stream):
        """Run the MCP server with custom streams."""
        await self.server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name=self.server_name,
                server_version="1.0.0",
                capabilities={}
            )
        )