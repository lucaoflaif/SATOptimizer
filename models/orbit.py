
from dataclasses import dataclass, field

from .task import Task, CandidateTask, VTW

@dataclass
class Orbit:
    id: int = field(init=False)
    candidate_tasks: list[CandidateTask]
    add_node_task = True
    add_sink_task = True

    def __post_init__(self):
        # add source and sink node
        if self.add_node_task: self.candidate_tasks.insert(0, Task(0,[],vtw=VTW(0,-1)),)
        if self.add_sink_task: self.candidate_tasks.append(Task(0,[],vtw=VTW(-1,1000000)))
    
    def get_candidate_tasks(self, with_source_node=False, with_sink_node=False):
        if with_source_node and with_sink_node: return self.candidate_tasks
        elif with_source_node: return self.candidate_tasks[:-1]
        elif with_sink_node: return self.candidate_tasks[1:]
        return self.candidate_tasks[1:-1]