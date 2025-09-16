from dataclasses import dataclass, field
from .target import Target

@dataclass
class CandidateTask:
    '''
    Task is what user wants, CandidatTask are all the intermediate tasks created by the solver 
    in order to set the problem and optimize for the best solution

    TODO: insted of these attributes it could be better to refer to an attribute with a Task instance
    '''
    target: Target
    start_time: int
    otw: int
    end_time:int = -1
    id: int = -1

    def __post_init__(self):
        self.end_time = self.start_time + self.otw

@dataclass
class VTW:
    start_time: int
    end_time: int

@dataclass
class Task: 
    otw: int
    target: Target
    id: int = field(init=False)
    vtw: VTW 