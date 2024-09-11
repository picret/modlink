from enum import Enum
from pydantic import Field
from modlink.action import Action, action_name

from example.context import ExampleContext


class BreakerWidth(Enum):
    LOW = 200
    MEDIUM = 100
    HIGH = 20
    EXTREME = 0


@action_name(
    name="breaker",
    description="Breaks the text into lines using predefined character widths.",
)
class BreakerAction(Action):
    width: BreakerWidth = Field(
        description="Number of characters to fit in a line.",
    )

    def perform(self, context: ExampleContext) -> str:
        words = context.text.split()
        result_lines = []

        if self.width == BreakerWidth.EXTREME:
            result_lines = words
        else:
            current_line = []
            total_chars = 0
            for word in words:
                prospective_length = total_chars + len(word) + len(current_line)
                if prospective_length > self.width.value:
                    result_lines.append(" ".join(current_line))
                    current_line = [word]
                    total_chars = len(word)
                else:
                    current_line.append(word)
                    total_chars = prospective_length
            if current_line:
                result_lines.append(" ".join(current_line))
        text = "\n".join(result_lines)
        context.text = text
        return text
