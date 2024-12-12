
from tsp_utils.general import *
import random
import math
import numpy as np 

def init_colony(data_model):
    num_cities = len(data_model["locations"])
    ant_list = []
    ant = 0
    
    for ant in data_model["locations"]:
        ant_route = []
        ant_route.append(data_model["locations"][ant])
        ant_list.append(ant_route)
    return ant_list

def select_city(ant_route,data_model,distance_matrix,pheromone_matrix, alpha, beta):
    last_city = ant_route[-1]
    probabilities = []
    unvisited = []
    for city in data_model["locations"]:
        if city in ant_route:
            continue
        else:
            distance = distance_matrix[last_city][city]
            attractiveness = (1/distance)**beta
            pheromone = (pheromone_matrix[last_city][city])**alpha
            probabilities.append(pheromone*attractiveness)
            unvisited.append(city)
    total_probability = sum(probabilities)
    probabilities = [p / total_probability for p in probabilities]

    next_city = np.random.choice(unvisited, p=probabilities)

    return next_city

def route_distance(route, distance_matrix):
    """Calculates the total distance of a route."""
    distance = 0.0
    num_cities = len(route)
    for i in range(num_cities):
        from_city = route[i]
        to_city = route[(i + 1) % num_cities]
        distance += distance_matrix[from_city][to_city]
    return distance

def pheromone_update(ant_list,pheromone_matrix,distance_matrix,rho,q_constant,data_model):
    for i in len(data_model["locations"]):
       for j in len(data_model["locations"]): 
           for ant in ant_list:
               if data_model["locations"][i][j] in ant_list[ant]:
                   distance = route_distance(ant_list[ant],distance_matrix)
                   deposit_pheromone = q_constant/distance
               else:
                   deposit_pheromone = 0
               delta_pheromone = delta_pheromone + deposit_pheromone
           updated_pheromone = (1 - rho)*pheromone_matrix[i][j] + delta_pheromone
           pheromone_matrix[i][j] = updated_pheromone
    return pheromone_matrix

def ant_colony(data_model,alpha = 1, beta = 2, rho = 0.1, q_constant = 20, generations = 100):

    distance_matrix = compute_euclidean_distance_matrix(data_model["locations"])
    num_cities = len(data_model["locations"])
    ant_list = init_colony(data_model)

    pheromone_matrix = np.ones((num_cities,num_cities))
    best_distance = 0
    solution = []

    for g in generations:
        for ant in ant_list:
            while len(ant_list[ant]) < num_cities:
                next_city = select_city(ant_list[ant],data_model,distance_matrix,pheromone_matrix, alpha, beta)
                ant_list[ant].append(next_city)
            distance = route_distance(ant_list[ant],distance_matrix)
            if best_distance == 0 or distance < best_distance:
                best_distance = distance
                solution = ant_list[ant]
        pheromone_matrix = pheromone_update(ant_list,pheromone_matrix,distance_matrix,rho,q_constant,data_model)
        ant_list.clear()
        ant_list = init_colony(data_model)
    return solution

if __name__ == "__main__":

    points = parse_input('ale_20cidades3D.txt')#generate_random_points(20,dim=3)
    data_model = create_data_model(points)
    solution = ant_colony(data_model, alpha = 1, beta = 2, rho = 0.1, q_constant = 20, generations = 100)
    solution[1].append(solution[1][0])
    print_route(solution[1])
    plot_locations_with_connections(data_model["locations"], solution[1])
    input("Press Enter to exit...\n")



