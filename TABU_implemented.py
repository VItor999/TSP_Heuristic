from tsp_utils.general import *
import random
import math
from collections import deque


def greedy_route(distance_matrix):
    """Creates a greedy route starting from the first city."""
    num_cities = len(distance_matrix)
    unvisited = set(range(num_cities))
    current_city = 0
    route = [current_city]
    unvisited.remove(current_city)

    while unvisited:
        # Find the closest unvisited city
        next_city = min(unvisited, key=lambda city: distance_matrix[current_city][city])
        route.append(next_city)
        unvisited.remove(next_city)
        current_city = next_city

    return route

def create_route(num_cities):
    """Creates a random tour (route) of the cities."""
    route = list(range(num_cities))
    random.shuffle(route)
    return route


def route_distance(route, distance_matrix):
    """Calculates the total distance of a route."""
    distance = 0.0
    num_cities = len(route)
    for i in range(num_cities):
        from_city = route[i]
        to_city = route[(i + 1) % num_cities]
        distance += distance_matrix[from_city][to_city]
    return distance


def swap_neighbor(route):
    """Performs a swap mutation on the route."""
    num_cities = len(route)
    city1, city2 = random.sample(range(num_cities), 2)
    route[city1], route[city2] = route[city2], route[city1]
    return route


def inversion_neighbor(route):
    """Performs an inversion mutation on the route."""
    start, end = sorted(random.sample(range(len(route)), 2))
    route[start:end] = route[start:end][::-1]
    return route


def scramble_neighbor(route):
    """Performs a scramble mutation on the route."""
    start, end = sorted(random.sample(range(len(route)), 2))
    subset = route[start:end]
    random.shuffle(subset)
    route[start:end] = subset
    return route


def neighborhood(route, neighborhood_size):
    """Generates a set of neighbors using random mutations."""
    neighbor_functions = [swap_neighbor]
    neighbors = []
    for _ in range(neighborhood_size):
        neighbor_func = random.choice(neighbor_functions)
        neighbor_route = neighbor_func(route[:])  # Copy the route
        neighbors.append(neighbor_route)
    return neighbors


def tabu_search(data_model=None, tabu_size=10, max_iter=100, neighborhood_size=20):
    """
    Executes the Tabu Search algorithm.

    :param data_model: The problem's data model.
    :type data_model: dict
    :param tabu_size: Maximum size of the tabu list.
    :type tabu_size: int
    :param max_iter: Maximum number of iterations.
    :type max_iter: int
    :param neighborhood_size: Number of neighbors to evaluate per iteration.
    :type neighborhood_size: int
    :return: A tuple with progress, the best route, and the best distance.
    :rtype: tuple
    """
    # Initialize the problem
    if data_model is None:
        data_model = create_data_model()
    num_cities = len(data_model["locations"])
    distance_matrix = compute_euclidean_distance_matrix(data_model["locations"])

    # Create the initial solution
    current_route = greedy_route(distance_matrix)
    #current_route = create_route(num_cities)
    current_distance = route_distance(current_route, distance_matrix)

    # Initialize the best solution
    best_route = current_route[:]
    best_distance = current_distance

    # Tabu list
    tabu_list = deque(maxlen=tabu_size)

    # Progress tracker
    progress = []

    for iteration in range(max_iter):
        # Generate neighbors and evaluate them
        neighbors = neighborhood(current_route, neighborhood_size)
        evaluated_neighbors = [
            (neighbor, route_distance(neighbor, distance_matrix)) for neighbor in neighbors
        ]
        evaluated_neighbors.sort(key=lambda x: x[1])  # Sort by distance (minimization)

        # Select the best non-tabu neighbor
        for neighbor, distance in evaluated_neighbors:
            if neighbor not in tabu_list or distance < best_distance:
                current_route = neighbor
                current_distance = distance
                break

        # Update the tabu list
        tabu_list.append(current_route)

        # Update the best solution
        if current_distance < best_distance:
            best_route = current_route[:]
            best_distance = current_distance

        # Record progress
        progress.append(best_distance)
        if iteration % 10 == 0 or iteration == max_iter - 1:
            print(f"Iteration {iteration}: Best Distance = {best_distance:.2f}")

    return progress, best_route, best_distance


if __name__ == "__main__":

    points = parse_input('ale_20cidades3D.txt')#generate_random_points(20,dim=3)
    data_model = create_data_model(points)
    solution = tabu_search(data_model, max_iter=100, neighborhood_size=500)
    solution[1].append(solution[1][0])
    print_route(solution[1])
    plot_locations_with_connections(data_model["locations"], solution[1])
    input("Press Enter to exit...\n")
