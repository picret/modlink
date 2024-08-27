from .example_agent import ExampleAgent, ExampleContext
from modlink.tools.agent_arg_parser import AgentArgParser


if __name__ == "__main__":
    # Run with python -m examples.example_cli
    agent = ExampleAgent()
    agent.attach(ExampleContext())
    arg_parser = AgentArgParser(agent)
    arg_parser.parse_and_perform()
    agent.detach()
