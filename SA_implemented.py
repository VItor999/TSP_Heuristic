from tsp_utils.general import *
from tsp_utils.mutation import *

#

# 2-opt move: reverses the order of cities between two random indices
def two_opt(route):
    new_route = route[:]
    i, j = sorted(random.sample(range(len(route)), 2))
    new_route[i:j+1] = reversed(route[i:j+1])
    return new_route

# Nearest Neighbor Initialization: Generates a good initial solution
def nearest_neighbor_init(distance_matrix):
    num_cities = len(distance_matrix)
    unvisited = list(range(num_cities))
    current_city = random.choice(unvisited)
    route = [current_city]
    unvisited.remove(current_city)
    
    while unvisited:
        nearest_city = min(unvisited, key=lambda city: distance_matrix[current_city][city])
        route.append(nearest_city)
        unvisited.remove(nearest_city)
        current_city = nearest_city
    
    return route

# Adaptive Cooling Schedule: Cools down faster if no improvement
def adaptive_cooling_schedule(temperature, improvement_count):
    if improvement_count == 0:
        return temperature * 0.99  # Cool down faster if no improvement
    else:
        return temperature * 0.95  # Slow down cooling if improvement happens

# Restart Solution: Randomly shuffle the current solution as a restart mechanism
def restart_solution(current_solution):
    new_solution = current_solution[:]
    random.shuffle(new_solution)
    return new_solution

def swap_neighbor(route):
    num_cities = len(route)
    city1 = random.randint(0, num_cities - 1)
    city2 = random.randint(0, num_cities - 1)
    route[city1], route[city2] = route[city2], route[city1]
    #first = route[0]
    #route[-1] = first
    return route

# Inversion Neighbor
def inversion_neighbor(route):
    start, end = sorted([random.randint(0, len(route)-1) for _ in range(2)])
    route[start:end] = route[start:end][::-1]
    #first = route[0]
    #route[-1] = first
    return route

def neighbor(route , temperature, mutation_temp):
    neighbor_functions = [
                swap_neighbor,
                inversion_neighbor
            ]
    if(temperature <= mutation_temp ):
        neighbor_func = swap_neighbor
    else:
        neighbor_func = inversion_neighbor
    neighbor_route = neighbor_func(route)
    return neighbor_route

import random
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
    #first = route[0]
    #route.append(first)
    return route


# Simulated Annealing with 2-opt and Nearest Neighbor Initialization
def simulated_annealing(distance_matrix, initial_temperature, cooling_rate, min_temperature, restart_threshold, neighborhood_size = 100, initial_route = None, num_cities = 20, mutation_temp = 1000):
    # Initialize with the Nearest Neighbor solution
    current_solution = []
    if (initial_route != None):
        current_solution = initial_route
    else:
        #current_solution = create_route(num_cities)
        current_solution = nearest_neighbor_init(distance_matrix)
    current_distance = route_distance(current_solution,distance_matrix)

    # Best solution found
    best_solution = current_solution[:]
    best_distance = current_distance

    temperature = initial_temperature
    iteration = 0
    improvement_count = 0
    no_improvement_iterations = 0  # Counter to track how long we've gone without improvement

    while temperature > min_temperature:
        # Generate a neighboring solution using 2-opt move
        for j in range(neighborhood_size):
            new_solution = neighbor(current_solution, temperature, mutation_temp)
            new_distance = route_distance(new_solution,distance_matrix)

            # Calculate the change in distance
            delta_distance = new_distance - current_distance

            # Accept the new solution if it's better or based on a probability depending on temperature
            if delta_distance < 0 or random.random() < math.exp(-delta_distance / temperature):
                current_solution = new_solution
                current_distance = new_distance
                improvement_count += 1
                no_improvement_iterations = 0  # Reset improvement counter if an improvement is found

                # Update the best solution found
                if current_distance < best_distance:
                    best_solution = current_solution[:]
                    best_distance = current_distance
            else:
                no_improvement_iterations += 1

        # Adaptive cooling schedule
        temperature = adaptive_cooling_schedule(temperature, improvement_count)
        iteration += 1

        # If stuck for too long, restart the search
        if no_improvement_iterations > restart_threshold:
            current_solution = restart_solution(current_solution)
            current_distance = route_distance(current_solution,distance_matrix)
            no_improvement_iterations = 0  # Reset the counter after restarting

    best_solution.append(best_solution[0])
    return best_solution, best_distance


if __name__ == "__main__":
    points = generate_random_points(20)
    data_model = create_data_model(points)
    distance_matrix = compute_euclidean_distance_matrix(data_model["locations"])
    initial_temperature = 100000
    cooling_rate = 1
    min_temperature = 1
    best_route, best_distance = simulated_annealing(distance_matrix, initial_temperature, cooling_rate, min_temperature, 10, mutation_temp= 0.5*initial_temperature)
    best_route.append(best_route[0])
    print(f"Best route: {best_route}")
    print(f"Best distance: {best_distance}")
    plot_locations_with_connections(data_model["locations"], best_route)
    input("Press Enter to exit...\n")