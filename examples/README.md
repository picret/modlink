## example_cli.py - Command-line interface for agents

After building agents you can integrate with [AgentArgParser](example_cli.py) to have full command-line support for your agents.

```bash
➜ python examples/example_cli.py -h
usage: example_cli.py [-h] {concat,replace} ...

Manages text state

positional arguments:
  {concat,replace}  Actions to perform.
    concat          Concatenates a string on the end of an existing text
    replace         Replaces the text with a new value.

options:
  -h, --help        show this help message and exit
```

## example_agent.py - Example Agent implementation

Here is an example of how you can define an agent. Once you have defined an agent, you can attach it to a context and interact with it. The agent will also describe it's capabilities in a machine and human readable format. This makes it possible for other agents to understand capabilities.


```bash
(modlink-env) ➜  modlink git:(main) ✗ python examples/example_agent.py
Agent description: {'name': 'example-agent', 'role': 'Manages text state', 'actions': [{'properties': {'action': {'type': 'string', 'value': 'replace', 'description': 'Constant value to indicate the action type.'}, 'text': {'description': 'The text to be used as a replacement.', 'title': 'Text', 'type': 'string'}}, 'required': ['action', 'text'], 'type': 'object', 'description': 'Replaces the text with a new value.'}, {'properties': {'action': {'type': 'string', 'value': 'concat', 'description': 'Constant value to indicate the action type.'}, 'text': {'description': 'The text to concatenate.', 'title': 'Text', 'type': 'string'}}, 'required': ['action', 'text'], 'type': 'object', 'description': 'Concatenates a string on the end of an existing text'}]}
Action: {'action': 'concat', 'text': 'Will be replaced.'}
Action: {'action': 'replace', 'text': 'Hello, '}
Action: {'action': 'concat', 'text': ' world!'}
Action result: Hello,  world!
```
