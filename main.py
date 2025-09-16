import multiprocessing as mp
import time
import itertools

from models import *
# ==== TARGET, TASK, ORBIT AND SATELLITES DEFINITION ====

rome = Target(n_of_requested_observations=7, 
                        name='rome',
                        rewards=[0,5,10,15,20,25,30,35,40,45,50])
paris = Target(n_of_requested_observations=4, 
                    name='paris',
                    rewards=[0,1,2,3,4])
#israel = Target(n_of_requested_observations=6,
#                name='israel',
#                rewards=[0,1,2,3,4,5,6,7])

#this is dummy visibility cone data that'll be replaced by the orbit mechanics calculations
tasks = [
    Task(vtw=VTW(start_time=220, end_time=220+450), otw=25, target = rome),
    Task(vtw=VTW(start_time=0, end_time=300), otw=20, target = paris),
    #Task(vtw=VTW(start_time=500, end_time=610), otw=20, target = israel),
]

candidate_tasks = TasksBuilder.build_candidate_tasks(tasks, dt=5, sorted_by='start_time')

orbit = Orbit(candidate_tasks=candidate_tasks)

satellite = Satellite(
    orbits=[orbit, ]
)

opt = Optimizer(
    satellites=[satellite,]
)
opt._set_ids()
candidate_tasks = opt.satellites[0].orbits[0].get_candidate_tasks(with_sink_node=False, with_source_node=False)

def on_generation(ga_instance): pass

def fitness_function(ga_instance, solution, solution_idx): 
    fitness = 0

    #scheduled tasks
    candidate_solution_tasks = list(itertools.compress(candidate_tasks, solution))

    # ===== NUMBER OF SUPERPOSITION ERRORS AMONG SCHEDULED TASKS FITNESS =====
    #for every scehduled task's superposition add a penalty, get a prize otherwise
    for prev_t, post_t in zip(candidate_solution_tasks[:-1], candidate_solution_tasks[1:]):
        if prev_t.end_time > post_t.start_time: 
            fitness -= 1000
        else:
            fitness += 10
        
    # ===== NUMBER OF SCHEDULED TASKS FITNESS =====
    for target in Target.get_instances():
        '''for each target we first count how many tasks are scheduled, then we assign a positive incremental fitness value 
        if this number is approching the number of requested observation. Otherwise we're scheduling more tasks than we need
        so a fitness penalty is set.
        
        EXAMPLE: if we want 5 tasks for target A and we scheduled 4 we set a fitness reward of [reward_set_for_4_obs]*4
        if we want 5 tasks for target B and we scheduled 7 we set a fitness penalty of -50*7
        
        So we're trying to assign a reward if we're going towards the number of the wanted scheduled. We set a penalty otherwise.'''
    
        num_of_scheduled_tasks = sum([1 for t in candidate_solution_tasks if t.target.name == target.name])
        if num_of_scheduled_tasks in range(target.n_of_requested_observations+1):
            fitness_constant = target.rewards[num_of_scheduled_tasks]
        else:
            fitness_constant = -50
        fitness += fitness_constant*num_of_scheduled_tasks
    
    return fitness

gene_space = []
#every gene can only assume the value 0 / 1 (not scheduled / scheduled)
for _ in range(len(candidate_tasks)): gene_space.append([0,1])

params = {
    # SOLUTION REPRESENTATION
    'gene_space': gene_space, 
    'num_genes': len(gene_space),

    # POPULATION PARAMETERS
    'num_generations': 500,
    'sol_per_pop': 100,

    # SELECTION PARAMETERS
    'num_parents_mating': 50,
    'parent_selection_type': "tournament",
    'keep_parents': 25,

    # GENETIC OPERATORS
    'crossover_type': "single_point",
    'mutation_type': "scramble",
    'mutation_percent_genes': 5,
    'stop_criteria' : ["saturate_50"],  # Stop when fitness saturates for 50 generations
    'parallel_processing': max(8, mp.cpu_count()),

    # FITNESS FUNCTION
    'fitness_func': fitness_function,

    # CALLBACKS
    'on_generation': on_generation,
}

opt.set_ga_params(params=params)

tic = time.process_time()
opt.run()
toc = time.process_time()

best_solution, best_fitness, best_solution_idx = opt.get_best_solution()

# TODO: make logging prettier. It's currently an "it just works" solution
print(f"{30*'='}\nsol: {best_solution}\n{30*'='}\nfitness: {best_fitness}\nsol_idx: {best_solution_idx}\ntime: {toc-tic} s")

print(30*'=')
for idx, sol in enumerate(best_solution):
    if sol: print(f"target: {candidate_tasks[idx].target.name}; start: {candidate_tasks[idx].start_time} s; end: {candidate_tasks[idx].end_time} s")