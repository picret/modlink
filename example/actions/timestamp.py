from datetime import date
from typing import Optional
from pydantic import Field
from modlink.action import Action, action_name

from example.context import ExampleContext


@action_name(
    name="timestamp",
    description="Adds a timestamp to the text.",
)
class TimestampAction(Action):
    transaction: Optional[date] = Field(
        description="Transaction ID for the action.",
    )

    def perform(self, context: ExampleContext) -> str:
        context.text = f"{self.transaction}: {context.text}"
        return context.text
