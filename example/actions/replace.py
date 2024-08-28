from pydantic import Field
from modlink.action import Action, action_name

from example.context import ExampleContext


@action_name(
    name="replace",
    description="Replaces the text with a new value.",
)
class ReplaceAction(Action):
    text: str = Field(description="The text to be used as a replacement.")

    def perform(self, context: ExampleContext) -> str:
        context.text = self.text
        return context.text
