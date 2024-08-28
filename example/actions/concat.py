from pydantic import Field
from modlink.action import Action, action_name

from example.context import ExampleContext


@action_name(
    name="concat",
    description="Concatenates a string on the end of an existing text",
)
class ConcatAction(Action):
    text: str = Field(description="The text to concatenate.")

    def perform(self, context: ExampleContext) -> str:
        context.text += self.text
        return context.text
