from typing import Protocol


class AIConsumerProtocol(Protocol):
    def generate_text(self, instructions: str, input: str, model: str):
        pass
