from enum import Enum
import re
import string
from typing import List, Optional
from pydantic import Field
from modlink.action import Action, action_name

from example.context import ExampleContext


class FilterOperation(Enum):
    LETTERS = "letters"
    DIGITS = "digits"
    SPACES = "spaces"
    PUNCTUATION = "punctuation"


@action_name(
    name="filter",
    description="Filters the text based on character types.",
)
class FilterAction(Action):
    words: Optional[List[str]] = Field(
        default=[],
        description="Array of words to filter from the text.",
    )
    operations: Optional[List[FilterOperation]] = Field(
        default=[],
        description="Array of filter types to use on the text.",
    )

    def perform(self, context: ExampleContext) -> str:
        for word in self.words:
            context.text = context.text.replace(word, "")

        if FilterOperation.LETTERS in self.operations:
            context.text = re.sub(r"[a-zA-Z]", "", context.text)
        if FilterOperation.DIGITS in self.operations:
            context.text = re.sub(r"[\d\s]", "", context.text)
        if FilterOperation.SPACES in self.operations:
            context.text = context.text.replace(" ", "")
        if FilterOperation.PUNCTUATION in self.operations:
            context.text = re.sub(
                f"[{re.escape(string.punctuation)}]", "", context.text
            )

        return context.text
