from dataclasses import dataclass, field

from .orbit import Orbit

@dataclass
class Satellite:
    orbits: list[Orbit]
    id: int = field(init=False)
    _counter: int = 0

    def __post_init__(self) -> None:
        self.id = type(self)._counter
        type(self)._counter += 1