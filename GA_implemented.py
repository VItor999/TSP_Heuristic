from tsp_utils.general import *

def create_route(num_cities):
    '''
    Creates a random tour (route) of the cities.

    :param num_cities: number of cities to visit
    :type num_cities: int 
    :return: list with a random tour of the cities 
    :rtype: list[int]
    '''
    
    route = list(range(num_cities))
    random.shuffle(route)
    return route

def initial_population(num_cities, population_size):
    '''
    Generates the initial population of routes.

    :param num_cities: number of cities to visit
    :type num_cities: int
    :param population_size: Number of beings in the population
    :type population_size: int
    :return: list containing the route for each member of the population
    :rtype: list[list[int]]
    '''
    
    return [create_route(num_cities) for _ in range(population_size)]

def route_distance(route, distance_matix):
    '''
    _summary_

    :param route: Tour; route to have total distance calculated
    :type route: list[int]
    :param distance_matix: Matrix with the distance form point to point
    :type distance_matix: dict
    :return: total distance of a route
    :rtype: float
    '''
    
    distance = 0.0
    num_cities = len(route)
    for i in range(num_cities):
        from_city = route[i]
        to_city = route[(i + 1) % num_cities]
        distance += distance_matix[from_city][to_city]
    return distance


def fitness(route, distance_matrix):
    '''
    Calculates the fitness of a route based on inverse of distance

    :param route: tour to be executed
    :type route: list[int]
    :param distance_matix: Matrix with the distance form point to point
    :type distance_matix: dict
    :return: metric to indicate how good is the route (the grater the better)
    :rtype: float
    '''
    
    return 1.0 / route_distance(route, distance_matrix)

def rank_routes(population, distance_matrix):
    '''
    Ranks routes in the population based on fitness

    :param population: current population
    :type population: list[list[int]]
    :param distance_matix: Matrix with the distance form point to point
    :type distance_matix: dict
    :return: population resorted based on best route 
    :rtype: list[list[int]]
    '''
    
    fitness_results = [(route, fitness(route, distance_matrix)) for route in population]
    return sorted(fitness_results, key=lambda x: x[1], reverse=True)

def selection(pop_ranked, elite_size = 5, tournament_size = 5):
    '''
    Selects parent routes using tournament selection

    :param pop_ranked: ranked population 
    :type pop_ranked: list[list[int]]
    :param elite_size: Size of the elite of the population, defaults to 5
    :type elite_size: int, optional
    :param tournament_size: Size of the tournament/number of elements selected to find the best to breed, defaults to 5
    :type tournament_size: int, optional
    :return: elements selected to breed
    :rtype: list[list[int]]
    '''
    
    selection_results = []
    for elite in range(elite_size):
        selection_results.append(pop_ranked[elite][0])
    for _ in range(len(pop_ranked) - elite_size):
        tournament = random.sample(pop_ranked, tournament_size)
        winner = max(tournament, key=lambda x: x[1])[0]
        selection_results.append(winner)
    return selection_results

def breed(parent1, parent2):
    '''
    Breeds two parents to generate a new elements.Performs Order Crossover (OX) to create a child route

    :param parent1: First parent
    :type parent1: list[int]
    :param parent2: Second parent
    :type parent2: list[int]
    :return: Newly generate child
    :rtype: list[int]
    '''
    
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
    '''
    Creates a new population through crossover.

    :param mating_pool: Selected elements to breed 
    :type mating_pool: list[list[int]]
    :param elite_size: Elite size/elements that will be copied directly, defaults to 5
    :type elite_size: int, optional
    :return: new part of the population
    :rtype: list[list[int]]
    '''
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
    '''
    Performs swap mutation on a route

    :param route: one element of the population
    :type route: list[int]
    :param mutation_rate: possibility of mutation, defaults to 0.01 (1%)
    :type mutation_rate: float, optional
    :return: mutated route/individual
    :rtype: list[int]
    '''
 
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
    '''
    Applies mutation to the population.

    :param population: Un-mutated population
    :type population: list[list[int]]
    :param mutation_rate: possibility of mutation, defaults to 0.01 (1%)
    :type mutation_rate: float, optional
    :return: Mutated population 
    :rtype: list[list[int]]
    '''
    
    mutated_pop = []
    for ind in range(len(population)):
        mutated_ind = mutate(population[ind],mutation_rate)
        mutated_pop.append(mutated_ind)
    return mutated_pop

def next_generation(current_gen, distance_matrix,mutation_rate = 0.01, tournament_size = 5, elite_size = 5):
    '''
    Creates the next generation.

    :param current_gen: Current population
    :type current_gen: list[list[int]]
    :param distance_matix: Matrix with the distance form point to point
    :type distance_matix: dict
    :param mutation_rate: _description_, defaults to 0.01
    :type mutation_rate: float, optional
    :param tournament_size: Size of the tournament/number of elements selected to find the best to breed, defaults to 5
    :type tournament_size: int, optional
    :param elite_size: Elite size/elements that will be copied directly, defaults to 5
    :type elite_size: int, optional
    :return: new generation 
    :rtype: list[list[int]]
    '''
    
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