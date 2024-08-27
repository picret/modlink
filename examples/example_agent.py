from typing import Optional
from pydantic import Field

import modlink as mk


class ExampleContext(mk.Context):
    _text: str = "Initial state"

    @property
    def text(self) -> str:
        return self._text


@mk.agent_name(
    name="example-agent",
    role="Manages text state",
)
class ExampleAgent(mk.Agent[ExampleContext]):
    """
    An example implementation of an Agent.
    """

    def attach(self, context: ExampleContext):
        super().attach(context)
        self._action_registry.add_all(
            ReplaceAction,
            ConcatAction,
            PadAction,
        )


@mk.action_name(
    name="replace",
    description="Replaces the text with a new value.",
)
class ReplaceAction(mk.Action):
    text: str = Field(description="The text to be used as a replacement.")

    def perform(self, context: ExampleContext) -> str:
        context._text = self.text
        print(f"Text result: {context._text}")
        return context._text


@mk.action_name(
    name="concat",
    description="Concatenates a string on the end of an existing text",
)
class ConcatAction(mk.Action):
    text: str = Field(description="The text to concatenate.")

    def perform(self, context: ExampleContext) -> str:
        context._text += self.text
        print(f"Action result: {context._text}")
        return context._text


@mk.action_name(
    name="pad",
    description="Pads the text with text.",
)
class PadAction(mk.Action):
    text: Optional[str] = Field(
        default=" ",
        description=("Text to pad with. Defaults to a space."),
    )
    start: Optional[int] = Field(
        default=0,
        description=(
            "Text multiplier to pad to the start of the text. " "Defaults to zero."
        ),
    )
    end: Optional[int] = Field(
        default=0,
        description=(
            "Text multiplier to add to the end of the text. " "Defaults to zero."
        ),
    )

    def perform(self, context: ExampleContext) -> str:
        text = context._text
        if self.start and self.start > 0:
            text = self.text * self.start + text
        if self.end and self.end > 0:
            text = text + self.text * self.end
        context._text = text

        print(f"Padded text result: {text}")
        return context._text


def example():
    # Run with python -m modlink.example_agent
    agent = ExampleAgent()
    agent.attach(ExampleContext())
    agent.perform(ReplaceAction(text="New state"))

    print(f"Agent description: {agent.describe()}")

    # Actions to build the string
    action_dicts = [
        {"action": "concat", "text": "Will be replaced."},
        {"action": "replace", "text": "Hello, "},
        {"action": "concat", "text": " world!"},
    ]
    for action_dict in action_dicts:
        print(f"Action: {action_dict}")
        action = agent.action_from_dict(action_dict)
        agent.perform(action)

    print(f"Action result: {agent.context.text}")
    agent.detach()


if __name__ == "__main__":
    # Run with python -m modlink.examples.example_agent
    example()
