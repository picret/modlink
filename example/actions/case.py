from enum import Enum
from typing import Optional
from pydantic import Field
from modlink.action import Action, action_name

from example.context import ExampleContext


class CaseOperation(Enum):
    UPPER = "upper"
    LOWER = "lower"
    TITLE = "title"
    CAPITALIZE = "capitalize"
    SWAPCASE = "swapcase"
    CASEFOLD = "casefold"


@action_name(
    name="case",
    description="Changes the case of the text.",
)
class CaseAction(Action):
    operation: Optional[CaseOperation] = Field(
        default=CaseOperation.UPPER,
        description="The type of operation to perform on the text.",
    )

    def perform(self, context: ExampleContext) -> str:
        if self.operation == CaseOperation.UPPER:
            context.text = context.text.upper()
        elif self.operation == CaseOperation.LOWER:
            context.text = context.text.lower()
        elif self.operation == CaseOperation.TITLE:
            context.text = context.text.title()
        elif self.operation == CaseOperation.CAPITALIZE:
            context.text = context.text.capitalize()
        elif self.operation == CaseOperation.SWAPCASE:
            context.text = context.text.swapcase()
        elif self.operation == CaseOperation.CASEFOLD:
            context.text = context.text.casefold()
        return context.text
