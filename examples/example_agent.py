from enum import Enum
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
            CaseAction,
        )


@mk.action_name(
    name="replace",
    description="Replaces the text with a new value.",
)
class ReplaceAction(mk.Action):
    text: str = Field(description="The text to be used as a replacement.")

    def perform(self, context: ExampleContext) -> str:
        context._text = self.text
        return context._text


@mk.action_name(
    name="concat",
    description="Concatenates a string on the end of an existing text",
)
class ConcatAction(mk.Action):
    text: str = Field(description="The text to concatenate.")

    def perform(self, context: ExampleContext) -> str:
        context._text += self.text
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
        if self.start and self.start > 0:
            context._text = self.text * self.start + context._text
        if self.end and self.end > 0:
            context._text = context._text + self.text * self.end
        return context._text


class CaseOperation(Enum):
    UPPER = "upper"
    LOWER = "lower"
    TITLE = "title"
    CAPITALIZE = "capitalize"
    SWAPCASE = "swapcase"
    CASEFOLD = "casefold"


@mk.action_name(
    name="case",
    description="Changes the case of the text.",
)
class CaseAction(mk.Action):
    operation: Optional[CaseOperation] = Field(
        default=CaseOperation.UPPER,
        description="The type of operation to perform on the text.",
    )

    def perform(self, context: ExampleContext) -> str:
        if self.operation == CaseOperation.UPPER:
            context._text = context._text.upper()
        elif self.operation == CaseOperation.LOWER:
            context._text = context._text.lower()
        elif self.operation == CaseOperation.TITLE:
            context._text = context._text.title()
        elif self.operation == CaseOperation.CAPITALIZE:
            context._text = context._text.capitalize()
        elif self.operation == CaseOperation.SWAPCASE:
            context._text = context._text.swapcase()
        elif self.operation == CaseOperation.CASEFOLD:
            context._text = context._text.casefold()
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
