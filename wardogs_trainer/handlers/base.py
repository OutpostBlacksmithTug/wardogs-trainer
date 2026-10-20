from abc import ABC, abstractmethod


class BaseHandler(ABC):
    """Feature handler invoked each tick of the trainer loop."""

    name: str = "unnamed"

    def __init__(self, mem, offsets, options: dict):
        self.mem = mem
        self.offsets = offsets
        self.options = options
        self.enabled = bool(options.get("enabled", False))

    @abstractmethod
    def tick(self) -> None:
        ...

    def shutdown(self) -> None:
        pass