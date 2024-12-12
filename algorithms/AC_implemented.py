

from tsp_utils.general import *
import random
import math
import numpy as np 

def create_city_order(data_model):
    num_cities = len(data_model["locations"])
    ordered_cities = []
    for city in range(num_cities):
        ordered_cities.append(city)
    return ordered_cities


def init_colony(ordered_cities):   
    ant_list = []
    ant = 0   
    for ant in ordered_cities:
        ant_route = []
        ant_route.append(ordered_cities[ant])
        ant_list.append(ant_route)
    return ant_list

def select_city(ant_route,ordered_cities,distance_matrix,pheromone_matrix, alpha, beta):
    last_city = ant_route[-1]
    #print(last_city)
    probabilities = []
    unvisited = []
    for city in ordered_cities:
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


               
def update_pheromone(ant_list,pheromone_matrix,distance_matrix,rho,q_constant):
    for i in range(len(pheromone_matrix)):
        for j in range(len(pheromone_matrix[i])):
            pheromone_matrix[i][j] *= (1 - rho)

    # Update pheromone for edges in the ant's path
    for ant in range(len(ant_list)):
        distance = route_distance(ant_list[ant],distance_matrix)
        deposit_pheromone = q_constant/distance
        for i in range(len(ant_list[ant]) - 1):
            city1 = ant_list[ant][i]
            city2 = ant_list[ant][i + 1]
            pheromone_matrix[city1][city2] += deposit_pheromone
            pheromone_matrix[city2][city1] += deposit_pheromone
    return pheromone_matrix

    


#def pheromone_update(ant_list,pheromone_matrix,distance_matrix,rho,q_constant,ordered_cities):
#    for i in len(ordered_cities):
#       for j in len(ordered_cities): 
#           for ant in ant_list:
#               if data_model["locations"][i][j] in ant_list[ant]:
#                   distance = route_distance(ant_list[ant],distance_matrix)
#                   deposit_pheromone = q_constant/distance
#               else:
#                   deposit_pheromone = 0
#               delta_pheromone = delta_pheromone + deposit_pheromone
#           updated_pheromone = (1 - rho)*pheromone_matrix[i][j] + delta_pheromone
#           pheromone_matrix[i][j] = updated_pheromone
#    return pheromone_matrix

def ant_colony(data_model,alpha = 1, beta = 2, rho = 0.1, q_constant = 20, generations = 100):

    distance_matrix = compute_euclidean_distance_matrix(data_model["locations"])
    num_cities = len(data_model["locations"])
    ordered_cities = create_city_order(data_model)
    ant_list = init_colony(ordered_cities)    
    pheromone_matrix = np.ones((num_cities,num_cities))
    best_distance = 0
    solution = []

    for g in range(generations):
        for ant in range(len(ant_list)):
            while len(ant_list[ant]) < num_cities:
                next_city = select_city(ant_list[ant],ordered_cities,distance_matrix,pheromone_matrix, alpha, beta)
                ant_list[ant].append(next_city)
            first_city = ant_list[ant][0]
            ant_list[ant].append(first_city)
            distance = route_distance(ant_list[ant],distance_matrix)
            if best_distance == 0 or distance < best_distance:
                best_distance = distance
                solution = ant_list[ant]
                print(best_distance)
        pheromone_matrix = update_pheromone(ant_list,pheromone_matrix,distance_matrix,rho,q_constant)
        ant_list.clear()
        ant_list = init_colony(ordered_cities)
    print(best_distance)    
    return solution

if __name__ == "__main__":

    points = parse_input('ale_99cidades3D.txt')#generate_random_points(20,dim=3)
    data_model = create_data_model(points)
    solution = ant_colony(data_model, alpha = 1, beta = 2, rho = 0.1, q_constant = 100, generations = 200)
    #solution[1].append(solution[1][0])
    print_route(solution)
    plot_locations_with_connections(data_model["locations"], solution)
    input("Press Enter to exit...\n")

