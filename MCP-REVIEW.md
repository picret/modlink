# MCP prototype preservation — 2026-10-10

The existing MCP adapter commit and local manual-test changes are preserved on
`km-add-mcp-tool`. They are not ready to merge:

- The manual example catches handler failures and falls back to a direct agent
  call. That does not verify the MCP transport/handler contract and can hide a
  broken adapter. Add an actual in-memory MCP client/server integration test.
- `{"action": name, **arguments}` allows arguments to override the selected tool
  name. Reject `action` in arguments or force the validated name after arguments.
- Schema conversion discards constraints, array items and nested object details.
  Preserve supported JSON Schema fields and cover nested/optional/enum inputs.

No server was started and no agent action was invoked during this review.
