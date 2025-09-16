from .task import CandidateTask

class TasksBuilder:
    @classmethod
    def build_candidate_tasks(cls, tasks, dt, sorted_by):
        candidate_tasks = []
        for task in tasks:
            for i in range(int((task.vtw.end_time - task.vtw.start_time - task.otw) / dt)+1): 
                candidate_tasks.append(
                    CandidateTask(target=task.target, 
                                  start_time=(i*dt)+task.vtw.start_time, 
                                  end_time=(i*dt)+task.vtw.start_time+task.otw,
                                  otw=task.otw,)
                )
        candidate_tasks = sorted(candidate_tasks, key=lambda task: getattr(task, sorted_by))
        return candidate_tasks
    