import numpy as np
import matplotlib.pyplot as plt
import random
from tsp_utils.general import *

def create_route(num_cities):
    """Creates a random tour (route) of the cities."""
    route = list(range(num_cities))
    random.shuffle(route)
    #print(route)
    return route

def initial_population(num_cities, population_size):
    """Generates the initial population of routes."""
    return [create_route(num_cities) for _ in range(population_size)]

def route_distance(route, distance_matix):
    """Calculates the total distance of a route."""
    distance = 0.0
    num_cities = len(route)
    for i in range(num_cities):
        from_city = route[i]
        to_city = route[(i + 1) % num_cities]
        distance += distance_matix[from_city][to_city]
    return distance

def fitness(route, distance_matrix):
    """Calculates the fitness of a route based on inverse of distance."""
    return 1.0 / route_distance(route, distance_matrix)

def rank_routes(population, distance_matrix):
    """Ranks routes in the population based on fitness."""
    fitness_results = [(route, fitness(route, distance_matrix)) for route in population]
    return sorted(fitness_results, key=lambda x: x[1], reverse=True)

def selection(pop_ranked, elite_size = 5, tournament_size = 5):
    """Selects parent routes using tournament selection."""
    selection_results = []
    for elite in range(elite_size):
        selection_results.append(pop_ranked[elite][0])
    for _ in range(len(pop_ranked) - elite_size):
        tournament = random.sample(pop_ranked, tournament_size)
        winner = max(tournament, key=lambda x: x[1])[0]
        selection_results.append(winner)
    return selection_results

def breed(parent1, parent2):
    """Performs Order Crossover (OX) to create a child route."""
    num_cities = len(parent1)
    child = [None] * num_cities

    # Select a subset from parent1
    gene_a = int(random.random() * num_cities)
    gene_b = int(random.random() * num_cities)

    start_gene = min(gene_a, gene_b)
    end_gene = max(gene_a, gene_b)

    # Copy the subset to the child
    child[start_gene:end_gene] = parent1[start_gene:end_gene]

    # Fill the remaining positions with genes from parent2
    parent2_genes = [gene for gene in parent2 if gene not in child]
    current_pos = 0
    for i in range(num_cities):
        if child[i] is None:
            child[i] = parent2_genes[current_pos]
            current_pos += 1

    return child

def breed_population(mating_pool, elite_size = 5):
    """Creates a new population through crossover."""
    children = []
    length = len(mating_pool)
    pool = random.sample(mating_pool, len(mating_pool))

    for i in range(elite_size):
        children.append(mating_pool[i])

    for i in range(elite_size, length):
        child = breed(pool[i - elite_size], pool[length - i - 1])
        children.append(child)
    return children

def mutate(route, mutation_rate=0.01):
    """Performs swap mutation on a route."""
    num_cites = len(route)
    for swapped in range(num_cites):
        if random.random() < mutation_rate:
            swap_with = int(random.random() * num_cites)

            city1 = route[swapped]
            city2 = route[swap_with]

            route[swapped] = city2
            route[swap_with] = city1
    return route

def mutate_population(population, mutation_rate=0.01 ):
    """Applies mutation to the population."""
    mutated_pop = []
    for ind in range(len(population)):
        mutated_ind = mutate(population[ind],mutation_rate)
        mutated_pop.append(mutated_ind)
    return mutated_pop

def next_generation(current_gen, distance_matrix,mutation_rate = 0.01, tournament_size = 5, elite_size = 5):
    """Creates the next generation."""
    pop_ranked = rank_routes(current_gen, distance_matrix)
    selection_results = selection(pop_ranked, elite_size, tournament_size)
    mating_pool = selection_results
    children = breed_population(mating_pool, elite_size)
    next_gen = mutate_population(children,mutation_rate)
    return next_gen

def GA_implemented(cities = None,population_size = 100, num_generations = 100, mutation_rate = 0.01,
                   tournament_size = 5, elite_size = 5):
    # Define the number of cities and the population size
    #locations = generate_form_points(4,"square")
    data_model = None
    if(cities == None):
        data_model = create_data_model()
    else:
        data_model = cities
    num_cities = len(data_model["locations"])
    

    # Calculate the distance matrix between all pairs of cities
    distance_matrix = compute_euclidean_distance_matrix(data_model["locations"])
    """Main function to run the Genetic Algorithm."""
    pop = initial_population(num_cities, population_size)
    progress = []

    print("Initial distance: " + str(1 / rank_routes(pop, distance_matrix)[0][1]))

    for i in range(num_generations):
        pop = next_generation(pop,distance_matrix,mutation_rate,tournament_size,elite_size)
        best_distance = 1 / rank_routes(pop,distance_matrix)[0][1]
        progress.append(best_distance)
        if i % 20 == 0:
            print(f"Generation {i:4d} distance: {best_distance:.2f}")

    print("Final distance: " + str(1 / rank_routes(pop, distance_matrix)[0][1]))
    best_route_index = rank_routes(pop, distance_matrix)[0][0]
    best_route = best_route_index
    best_route.append(best_route[0])
    return (progress, best_route,  best_distance)


if __name__ == "__main__":
    data_model = create_data_model()
    num_cities = len(data_model["locations"])
    solution = GA_implemented(num_generations=50)
    print_route(solution[1])
    plot_locations_with_connections(data_model["locations"], solution[1])
    input("Press Enter to exit...\n")