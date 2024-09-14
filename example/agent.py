from modlink import Agent, agent_name
from modlink.tools.agent_arg_parser import AgentArgParser
import logging

from example.context import ExampleContext


@agent_name(
    name="example-agent",
    role="Edits text state",
)
class ExampleAgent(Agent[ExampleContext]):
    """
    An example implementation of an Agent.
    """

    def attach(self, context: ExampleContext):
        super().attach(context)

        # Add all the actions from a package to the agent
        self._action_registry.add_package("example.actions")

        # Alternatively, add actions individually
        # self._action_registry.add_action(ReplaceAction)


if __name__ == "__main__":
    # Run with python agent.py
    logging.basicConfig(level=logging.DEBUG)

    agent = ExampleAgent()
    agent.attach(ExampleContext())
    result = AgentArgParser(agent).parse_and_perform()
    print(f"Action result: {result}")
    agent.detach()
