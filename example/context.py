from modlink import Context


class ExampleContext(Context):
    DEFAULT_TEXT = "9035 Village Dr, Yosemite Valley, CA 95389, U.S.A."

    _text: str = DEFAULT_TEXT

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, value: str):
        self._text = value
