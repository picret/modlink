from argparse import Namespace
import unittest
from unittest.mock import patch
from example.actions.replace import ReplaceAction
from example.actions.timestamp import TimestampAction
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
        """Test the replace action is parsed correctly when context is present."""
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
        """Test the pad action is parsed correctly when context is present."""
        context = ExampleContext()
        self.agent.attach(context)
        text: str = self.parser.parse_and_perform()
        self.assertEqual(text, f"xxx{ExampleContext.DEFAULT_TEXT}x")

    @patch(
        "argparse.ArgumentParser.parse_args",
        return_value=Namespace(action="pad", end=3, text=" is padded"),
    )
    def test_pad_action_optional_parameters(self, _):
        """Test the pad action is parsed correctly when context is present."""
        context = ExampleContext()
        self.agent.attach(context)
        text: str = self.parser.parse_and_perform()
        self.assertEqual(
            text, f"{ExampleContext.DEFAULT_TEXT} is padded is padded is padded"
        )

    @patch(
        "argparse.ArgumentParser.parse_args",
        return_value=Namespace(action="case", operation="upper"),
    )
    def test_case_action_enum_parameters(self, _):
        """Test the replace action is parsed correctly when context is present."""
        context = ExampleContext()
        self.agent.attach(context)
        text: str = self.parser.parse_and_perform()
        self.assertEqual(text, ExampleContext.DEFAULT_TEXT.upper())

    @patch(
        "argparse.ArgumentParser.parse_args",
        return_value=Namespace(action="breaker", width=20),
    )
    def test_breaker_action_integer_enum_parameters(self, _):
        """Test the breaker action to read enum int types."""
        context = ExampleContext()
        context.text = "This is a long text that should be broken into lines"
        self.agent.attach(context)
        text: str = self.parser.parse_and_perform()
        self.assertEqual(
            text, "This is a long\ntext that should\nbe broken into\nlines"
        )

    @patch(
        "argparse.ArgumentParser.parse_args",
        return_value=Namespace(
            action="filter",
            words=["Dr", "CA", "U.S.A."],
            operations=["punctuation", "digits"],
        ),
    )
    def test_filter_action_array_parameters(self, _):
        """Test the filter action is parsed correctly when context is present."""
        context = ExampleContext()
        context.text = "9035 Village Dr, Yosemite Valley, CA 95389, U.S.A."
        self.agent.attach(context)
        text: str = self.parser.parse_and_perform()
        self.assertEqual(text, "VillageYosemiteValley")

    def test_action_with_action_field(self):
        """Test the a word like trans-action which contains action in the field."""
        context = ExampleContext()
        context.text = "Today is the day."
        self.agent.attach(context)
        self.parser = AgentArgParser(self.agent)

        result: TimestampAction = self.parser.parse_args(
            args=[
                "timestamp",
                "--transaction",
                "2024-11-01",
            ],
        )
        self.assertEqual(str(result.transaction), "2024-11-01")


if __name__ == "__main__":
    unittest.main()
