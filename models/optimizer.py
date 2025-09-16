import pygad

class Optimizer:
    def __init__(self, satellites):
        self.satellites = satellites

        self.ga_instance = None

    def _set_ids(self):
        for satellite in self.satellites:
            _orbit_id = 0
            for orbit in satellite.orbits:
                orbit.id = _orbit_id
                _orbit_id += 1

                _task_id = 0
                for task in orbit.candidate_tasks:
                    task.id = _task_id
                    _task_id += 1

    def set_ga_params(self, params):
        self.ga_instance = pygad.GA(**params)
    
    def get_best_solution(self):
        return self.ga_instance.best_solution()

    def run(self):
        self.ga_instance.run()