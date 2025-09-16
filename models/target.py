from dataclasses import dataclass, field
from typing import ClassVar, List

@dataclass
class Target:
    n_of_requested_observations: int
    name: str
    id: int = field(init=False)
    rewards: list[int]

    #every time an istance of Target is created an 
    #incrementally id is assigned to the istance itself (id = 0,1,2,..) 
    #TODO from 0,1,.. to 1,2,..
    _counter: int = 1

    # Class-level registry to hold all instances
    _instances: ClassVar[List["Target"]] = []

    def __post_init__(self) -> None:
        self.id = type(self)._counter
        type(self)._counter += 1

        if len(self.rewards) <= self.n_of_requested_observations: raise ValueError()

        # Add the newly created instance to the registry
        type(self)._instances.append(self)

    @classmethod
    def get_instances(cls) -> List["Target"]:
        """Return all instances of this dataclass"""
        return cls._instances