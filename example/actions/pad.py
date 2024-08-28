from typing import Optional
from pydantic import Field
from modlink.action import Action, action_name

from example.context import ExampleContext


@action_name(
    name="pad",
    description="Pads the text with text.",
)
class PadAction(Action):
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
            context.text = self.text * self.start + context.text
        if self.end and self.end > 0:
            context.text = context.text + self.text * self.end
        return context.text
