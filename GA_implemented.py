from tsp_utils.general import *
from tsp_utils.Being import Being

#TODO List:
#  - MUST: Create class for each solution/being in the population. 
#  - MUST: Fill this being data accordingly 
#  - MUST: Make some more sense of the code implement, somehow I think the population is getting smaller? 
#  - EXTRA: Try to make the algorithm better. Right now is working "ok"


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
    population = []
    for _ in range(population_size):
        b = Being(create_route(num_cities), [0,0] , 0, 0)
        population.append(b)
    return population

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
    fitness_results = []
    for being in population:
        f = fitness(being.route, distance_matrix)
        being.fitness = f
        fitness_results.append(f)
   
    sorted_population = sort_population_by_fitness(population)
    return sorted_population

def sort_population_by_fitness(population):
    """Sort population of beings by fitness in ascending order."""
    # Sort the population in place based on the fitness attribute
    population.sort(key=lambda being: being.fitness, reverse=True) 
    return population

def selection(pop_ranked, elite_size = 3, tournament_size = 3):
    '''
    Selects parent routes using tournament selection

    :param pop_ranked: ranked population 
    :type pop_ranked: list[list[int]]
    :param elite_size: Size of the elite of the population, defaults to 3
    :type elite_size: int, optional
    :param tournament_size: Size of the tournament/number of elements selected to find the best to breed, defaults to 3
    :type tournament_size: int, optional
    :return: elements selected to breed
    :rtype: list[list[int]]
    '''
    
    selection_results = []
    for elite in range(elite_size):
        selection_results.append(pop_ranked[elite])
    for _ in range(len(pop_ranked) - elite_size):
        tournament_candidates = random.sample(pop_ranked, tournament_size)
        sorted = sort_population_by_fitness(tournament_candidates)
        winner = sorted[0]
        selection_results.append(winner)
    return selection_results

def breed(parent1, parent2, gen):
    '''
    Breeds two parents to generate a new elements.Performs Order Crossover (OX) to create a child route

    :param parent1: First parent
    :type parent1: list[int]
    :param parent2: Second parent
    :type parent2: list[int]
    :return: Newly generate child
    :rtype: list[int]
    '''
    
    num_cities = len(parent1.route)
    child_route = [None] * num_cities

    # Select a subset from parent1
    gene_a = int(random.random() * num_cities)
    gene_b = int(random.random() * num_cities)

    start_gene = min(gene_a, gene_b)
    end_gene = max(gene_a, gene_b)

    # Copy the subset to the child
    child_route[start_gene:end_gene] = parent1.route[start_gene:end_gene]

    # Fill the remaining positions with genes from parent2
    parent2_genes = [gene for gene in parent2.route if gene not in child_route]
    current_pos = 0
    for i in range(num_cities):
        if child_route[i] is None:
            child_route[i] = parent2_genes[current_pos]
            current_pos += 1
    parents_ids = [parent1.id, parent2.id]
    mutation = 0
    
    child = Being(child_route, parents_ids, mutation, gen)
    return child

def breed_population(mating_pool, elite_size = 3, gen = 0):
    '''
    Creates a new population through crossover.

    :param mating_pool: Selected elements to breed 
    :type mating_pool: list[list[int]]
    :param elite_size: Elite size/elements that will be copied directly, defaults to 3
    :type elite_size: int, optional
    :return: new part of the population
    :rtype: list[list[int]]
    '''
    children = []
    length = len(mating_pool)
    pool = random.sample(mating_pool, len(mating_pool))

    #direct copy of the elite
    for i in range(elite_size):
        children.append(mating_pool[i])

    invalid_new_child = True
    #the rest
    for i in range(elite_size, length):
        while (invalid_new_child):
            child = breed(pool[i - elite_size], pool[length - i - 1], gen)
            invalid_new_child = False
            for valid_child in children:
                if(valid_child == child):
                    invalid_new_child = True
        children.append(child)
        invalid_new_child = True
    return children

# Swap Mutation
def swap_mutation(route):
    num_cities = len(route)
    city1 = random.randint(0, num_cities - 1)
    city2 = random.randint(0, num_cities - 1)
    route[city1], route[city2] = route[city2], route[city1]
    return route

# Inversion Mutation
def inversion_mutation(route):
    start, end = sorted([random.randint(0, len(route)-1) for _ in range(2)])
    route[start:end] = route[start:end][::-1]
    return route

# Scramble Mutation
def scramble_mutation(route):
    start, end = sorted([random.randint(0, len(route)-1) for _ in range(2)])
    subset = route[start:end]
    random.shuffle(subset)
    route[start:end] = subset
    return route

# Insertion Mutation
def insertion_mutation(route):
    city_index = random.randint(0, len(route)-1)
    city = route.pop(city_index)
    insert_at = random.randint(0, len(route)-1)
    route.insert(insert_at, city)
    return route

# Displacement Mutation
def displacement_mutation(route):
    start, end = sorted([random.randint(0, len(route)-1) for _ in range(2)])
    segment = route[start:end]
    del route[start:end]
    insert_at = random.randint(0, len(route)-1)
    route[insert_at:insert_at] = segment
    return route


# Randomly perform one mutation
def mutate(being, mutation_rate=0.01):
    """
    Randomly selects and performs one of the mutation algorithms on a being's route.
    """
    route = being.route
    for i in range(10):
        if random.random() < mutation_rate:
            mutation_functions = [
                swap_mutation,
                inversion_mutation,
                scramble_mutation,
                ##insertion_mutation,
                #displacement_mutation,
            ]
            mutation_func = random.choice(mutation_functions)
            route = mutation_func(route)
            being.update_mutation_number(1,mutation_func.__name__)
            being.route = route
    return being



def mutate_population(population, mutation_rate=0.01, elite_size = 3 ):
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
   
    for i in range(elite_size):
        mutated_pop.append(population[i])
    invalid_mutation = True
    length = len(population)
    #the rest
    for i in range(elite_size, length):
        while (invalid_mutation):
            mutated = mutate(population[i],mutation_rate)
            invalid_mutation = False
            for valid_being in mutated_pop:
                if(valid_being == mutated):
                    invalid_mutation = True
        mutated_pop.append(mutated)
        invalid_mutation = True
    return mutated_pop

def next_generation(genID, current_gen, distance_matrix,mutation_rate = 0.01, tournament_size = 3, elite_size = 3):
    '''
    Creates the next generation.

    :param current_gen: Current population
    :type current_gen: list[list[int]]
    :param distance_matix: Matrix with the distance form point to point
    :type distance_matix: dict
    :param mutation_rate: possibility of mutation, defaults to 0.01
    :type mutation_rate: float, optional
    :param tournament_size: Size of the tournament/number of elements selected to find the best to breed, defaults to 3
    :type tournament_size: int, optional
    :param elite_size: Elite size/elements that will be copied directly, defaults to 3
    :type elite_size: int, optional
    :return: new generation 
    :rtype: list[list[int]]
    '''
    
    pop_ranked = rank_routes(current_gen, distance_matrix)
    selection_results = selection(pop_ranked, elite_size, tournament_size)
    mating_pool = selection_results
    children = breed_population(mating_pool, elite_size, genID)
    next_gen = mutate_population(children,mutation_rate)
    return next_gen

def GA_implemented(data_model = None,population_size = 100, num_generations = 100, mutation_rate = 0.01,
                   tournament_size = 3, elite_size = 3):
    '''
    Execute the genetic algorithm (GA) proposed

    :param cities: postion of the cities, defaults to None
    :type cities: list[tuple(int,int)], optional
    :param population_size: Number of beings in the population, defaults to 100
    :type population_size: int, optional
    :param num_generations: Number of the generations to run the GA, defaults to 100
    :type num_generations: int, optional
    :param mutation_rate: possibility of mutation, defaults to 0.01
    :type mutation_rate: float, optional
    :param tournament_size: Size of the tournament/number of elements selected to find the best to breed, defaults to 3
    :type tournament_size: int, optional
    :param elite_size: Elite size/elements that will be copied directly, defaults to 3
    :type elite_size: int, optional
    :return: tuple with a list of the distances for each generation, the best route and the distance for the best route
    :rtype: tuple(list[int], list[int], int)
    '''
    Being.reset_ids()
    # Define the number of cities and the population size
    #locations = generate_form_points(4,"square")
    if(data_model == None):
        data_model = create_data_model()
        
    num_cities = len(data_model["locations"])
    

    # Calculate the distance matrix between all pairs of cities
    distance_matrix = compute_euclidean_distance_matrix(data_model["locations"])
    
    pop = initial_population(num_cities, population_size)
    progress = []

    print("Initial distance: " + str(1 / rank_routes(pop, distance_matrix)[0].fitness))

    for i in range(num_generations):
        pop = next_generation(i+1,pop,distance_matrix,mutation_rate,tournament_size,elite_size)
        best_distance = 1 / rank_routes(pop,distance_matrix)[0].fitness
        progress.append(best_distance)
        if i % 20 == 0:
            print(f"Generation {i:4d} distance: {best_distance:.2f}")

    pop = rank_routes(pop, distance_matrix)
    best_route = (pop[0].route)
    best_route.append(best_route[0])
    print("Final distance: " + str(1 / pop[0].fitness))
    print(pop[0].get_info())
    return (progress, best_route,  best_distance)


if __name__ == "__main__":
    points = generate_form_points(10, "square")
    data_model = create_data_model(points)
    solution = GA_implemented(data_model,num_generations=30)
    print_route(solution[1])
    plot_locations_with_connections(data_model["locations"], solution[1])
    input("Press Enter to exit...\n")