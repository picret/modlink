## Command-line interface for agents

After building agents you can integrate with [AgentArgParser](agent.py) to have full command-line support for your agents.

```bash
➜ python example/agent.py -h
usage: agent.py [-h] {case,concat,pad,replace} ...

Edits text state

positional arguments:
  {case,concat,pad,replace}
                        Actions to perform.
    case                Changes the case of the text.
    concat              Concatenates a string on the end of an existing text
    pad                 Pads the text with text.
    replace             Replaces the text with a new value.

options:
  -h, --help            show this help message and exit
```
