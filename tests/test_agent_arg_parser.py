from argparse import Namespace
import unittest
from unittest.mock import patch
from example.actions.replace import ReplaceAction
from example.agent import ExampleAgent
from example.context import ExampleContext
from modlink.tools import AgentArgParser


class TestAgentArgParser(unittest.TestCase):

    def setUp(self):
        self.agent = ExampleAgent()  # Assuming this doesn't set a context by default
        self.parser = AgentArgParser(self.agent)

    def test_runtime_error_on_missing_context(self):
        """Test that RuntimeError is raised when the agent has no context."""
        with self.assertRaises(RuntimeError):
            self.parser.parse_args()

    @patch(
        "argparse.ArgumentParser.parse_args",
        return_value=Namespace(action="replace", text="New Text State"),
    )
    def test_replace_action_with_context(self, _):
        """Test that replace action is parsed correctly when context is present."""
        context = ExampleContext()
        self.agent.attach(context)
        action: ReplaceAction = self.parser.parse_args()

        self.assertIsInstance(action, ReplaceAction)
        self.assertEqual(action.text, "New Text State")

    @patch(
        "argparse.ArgumentParser.parse_args",
        return_value=Namespace(action="pad", start=3, end=1, text="x"),
    )
    def test_pad_action(self, _):
        """Test that replace action is parsed correctly when context is present."""
        context = ExampleContext()
        self.agent.attach(context)
        text: str = self.parser.parse_and_perform()
        self.assertEqual(text, "xxxInitial statex")

    @patch(
        "argparse.ArgumentParser.parse_args",
        return_value=Namespace(action="pad", end=3, text=" is padded"),
    )
    def test_pad_action_optional_parameters(self, _):
        """Test that replace action is parsed correctly when context is present."""
        context = ExampleContext()
        self.agent.attach(context)
        text: str = self.parser.parse_and_perform()
        self.assertEqual(text, "Initial state is padded is padded is padded")

    @patch(
        "argparse.ArgumentParser.parse_args",
        return_value=Namespace(action="case", operation="upper"),
    )
    def test_case_action_enum_parameters(self, _):
        """Test that replace action is parsed correctly when context is present."""
        context = ExampleContext()
        self.agent.attach(context)
        text: str = self.parser.parse_and_perform()
        self.assertEqual(text, "INITIAL STATE")


if __name__ == "__main__":
    unittest.main()
