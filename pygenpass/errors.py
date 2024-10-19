class ArgsParsingError(Exception):
    def __init__(self, message: str, code: int = 100) -> None:
        super().__init__(message)
        self.code: int = code

    def __str__(self) -> str:
        return f"[ArgsParsingError]: {self.args[0]}"

    def __repr__(self) -> str:
        return f"[ArgsParsingError ({self.code})]: {self.args[0]}"


class GeneratingPasswordError(Exception):
    def __init__(self, message: str, code: int = 200) -> None:
        super().__init__(message)
        self.code = code

    def __str__(self):
        return f"[GeneratingPasswordError]: {self.args[0]}"

    def __repr__(self) -> str:
        return f"[GeneratingPasswordError ({self.code})]: {self.args[0]}"
