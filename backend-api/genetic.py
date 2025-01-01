import numpy as np
import pygad

def distance_matrix(coords):
    n = len(coords)
    dist = np.zeros((n,n))
    for i in range(n):
        for j in range(n):
            if i != j:
                dist[i][j] = np.linalg.norm(np.array(coords[i]) - np.array(coords[j]))
    return dist

def fitness_func(solution, sol_idx, dist_mat):
    total_dist = 0
    for i in range(len(solution) - 1):
        total_dist += dist_mat[solution[i]][solution[i+1]]
    return 1.0 / (total_dist + 1e-6)

def run_genetic(coords):
    dist_mat = distance_matrix(coords)
    gene_space = range(len(coords))
    ga_instance = pygad.GA(
        num_generations=50,
        num_parents_mating=5,
        fitness_func=lambda s, idx: fitness_func(s, idx, dist_mat),
        sol_per_pop=10,
        num_genes=len(coords),
        gene_type=int,
        init_range_low=0,
        init_range_high=len(coords)-1,
        gene_space=gene_space,
        mutation_probability=0.1,
        crossover_type="single_point",
        mutation_type="random"
    )
    ga_instance.run()
    solution, solution_fitness, _ = ga_instance.best_solution()
    return solution, solution_fitness
