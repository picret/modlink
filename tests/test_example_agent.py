import unittest

from modlink import Action, action_name, Context
from examples.example_agent import ExampleAgent, ExampleContext, ReplaceAction


class TestExampleAgent(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.agent = ExampleAgent()
        self.context = ExampleContext()
        self.agent.attach(self.context)

    def tearDown(self):
        self.agent.detach()

    def test_agent_description(self):
        """Test the agent description is correct."""
        description = self.agent.describe()
        self.assertEqual(description["name"], "example-agent")
        self.assertEqual(description["role"], "Manages text state")
        self.assertEqual(len(description["actions"]), 4)

    def test_perform_action(self):
        """Test the agent can perform an action."""
        action = ReplaceAction(text="Action performed successfully")

        text = self.agent.perform(action)

        self.assertEqual(action.text, self.context.text)
        self.assertEqual(action.text, text)

    async def test_perform_async_action(self):
        """Test the agent can perform an action asynchronously."""
        self.agent.attach(self.context)
        action = ReplaceAction(text="Async action performed successfully")

        text = await self.agent.perform_async(action)

        self.assertEqual(action.text, self.context.text)
        self.assertEqual(action.text, text)

    def test_unsupported_action(self):
        """Test an unsupported action is performed."""

        @action_name(
            name="unknown_action",
            description="An action that is not supported by the agent",
        )
        class UnknownAction(Action):
            def perform(self, _: Context) -> None:
                pass

        action = UnknownAction()
        with self.assertRaises(ValueError) as context:
            self.agent.perform(action)
        self.assertEqual(str(context.exception), "Unsupported action: unknown_action")

    def test_needs_action_name(self):
        """Test an action is not decorated with @action_name."""

        class IncorrectAction(Action):
            def perform(self, _: Context) -> None:
                pass

        with self.assertRaises(RuntimeError) as context:
            action = IncorrectAction()
            self.agent.perform(action)
        self.assertEqual(
            str(context.exception),
            "IncorrectAction must be decorated by @action_name",
        )

    def test_detach_agent(self):
        """Test that the agent can be detached from a context."""
        self.agent.detach()
        with self.assertRaises(RuntimeError) as context:
            self.agent.context
        self.assertEqual(str(context.exception), "Agent is not attached to any context")


if __name__ == "__main__":
    unittest.main()
