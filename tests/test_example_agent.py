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
        description = self.agent.describe()
        self.assertEqual(description["name"], "example-agent")
        self.assertEqual(description["role"], "Manages text state")
        self.assertEqual(len(description["actions"]), 3)

    def test_perform_action(self):
        action = ReplaceAction(text="Action performed successfully")
        self.agent.perform(action)
        self.assertEqual(action.text, self.context.text)

    async def test_perform_async_action(self):
        self.agent.attach(self.context)
        action = ReplaceAction(text="Async action performed successfully")
        await self.agent.perform_async(action)
        self.assertEqual(action.text, self.context.text)

    def test_unsupported_action(self):
        @action_name(
            name="fake-action",
            description="An action that is not supported by the agent",
        )
        class FakeAction(Action):
            def perform(self, _: Context) -> None:
                pass

        action = FakeAction()
        with self.assertRaises(ValueError) as context:
            self.agent.perform(action)
        self.assertEqual(str(context.exception), "Unsupported action: fake-action")

    def test_needs_action_name(self):
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
        self.agent.detach()
        with self.assertRaises(RuntimeError) as context:
            self.agent.context
        self.assertEqual(str(context.exception), "Agent is not attached to any context")


if __name__ == "__main__":
    unittest.main()
