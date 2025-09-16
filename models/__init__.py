from .taskbuilder import *
from .optimizer import *
from .satellite import *
from .target import *
from .orbit import *
from .task import *

'''
====== EXAMPLE USAGE OF THE MODULE ======

rome = Target(n_of_requested_observations=10, 
                    name='rome',
                    rewards=[0,5,10,15,20,25,30,35,40,45,50])
paris = Target(n_of_requested_observations=2, 
                    name='paris',
                    rewards=[0,1,2])

tasks = [
    Task(vtw=VTW(start_time=0, end_time=50), otw=25, target = rome),
    Task(vtw=VTW(start_time=30, end_time=80), otw=20, target = paris),
]

candidate_tasks = TasksBuilder.build_candidate_tasks(tasks)

orbit = Orbit(candidate_tasks=candidate_tasks)
orbit_two = Orbit(tasks = tasks[9:])
satellite = Satellite(
    orbits=[orbit, orbit_two]
)
satellite_two = Satellite(
    orbits=[orbit_three]
)

opt = Optimizer(
    satellites=[satellite, satellite_two],
)
opt._set_ids()
'''