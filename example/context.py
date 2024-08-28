from modlink import Context


class ExampleContext(Context):
    _text: str = "Initial state"

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, value: str):
        self._text = value
