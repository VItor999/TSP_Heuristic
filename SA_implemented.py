from tsp_utils.general import *
from tsp_utils.SA_Being import SA_Being
import math



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

def route_distance(route, distance_matrix):
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
        distance += distance_matrix[from_city][to_city]
    return distance

# Swap Neighbor
def swap_neighbor(route):
    num_cities = len(route)
    city1 = random.randint(0, num_cities - 1)
    city2 = random.randint(0, num_cities - 1)
    route[city1], route[city2] = route[city2], route[city1]
    return route

# Inversion Neighbor
def inversion_neighbor(route):
    start, end = sorted([random.randint(0, len(route)-1) for _ in range(2)])
    route[start:end] = route[start:end][::-1]
    return route

# Scramble Neighbor
def scramble_neighbor(route):
    start, end = sorted([random.randint(0, len(route)-1) for _ in range(2)])
    subset = route[start:end]
    random.shuffle(subset)
    route[start:end] = subset
    return route


# Displacement Neighbor
def displacement_neighbor(route):
    start, end = sorted([random.randint(0, len(route)-1) for _ in range(2)])
    segment = route[start:end]
    del route[start:end]
    insert_at = random.randint(0, len(route)-1)
    route[insert_at:insert_at] = segment
    return route



def neighbor(route):
    neighbor_functions = [
                swap_neighbor,
                inversion_neighbor,
                scramble_neighbor,
                displacement_neighbor,
            ]
    neighbor_func = random.choice(neighbor_functions)
    neighbor_route = neighbor_func(route)
    return neighbor_route

def neighborhood(being, neighborhood_size, distance_matrix):
    distance = being.distance
    route = being.current_route
    for j in neighborhood_size:
        neighbor_route = neighbor(route)
        neighbor_distance = route_distance(neighbor_route,distance_matrix)
        if (neighbor_distance < distance):
            being.set_current_route(neighbor_route)
            being.distance = neighbor_distance
        else:
            compare = random.uniform(0, 1)
            temp_function = (distance-neighbor_distance)/being.temperature
            if(math.exp(temp_function)>compare):
                being.set_current_route(neighbor_route)
                being.distance = neighbor_distance
        distance = being.distance
        if (distance < being.best_distance):
            being.set_best_route
            being.best_distance = distance
        
        
def GA_implemented(data_model = None,movement_percentage = 0.15, worse_solutions = 0.05, ro = 1,
                   beta = 0.8, sigma = 0.15, cooling_constant = True):
  
    SA_Being.reset_ids()
    # Define the number of cities 
    #locations = generate_form_points(4,"square")
    if(data_model == None):
        data_model = create_data_model()
        
    num_cities = len(data_model["locations"])

    # Calculate the distance matrix between all pairs of cities
    distance_matrix = compute_euclidean_distance_matrix(data_model["locations"])
    


    first_route = SA_Being(create_route(num_cities), [0,0] , 0, 0)
    first_distance = route_distance(first_route, distance_matrix)

    progress = []

    print("Initial distance: " + str(first_distance))

    

    progress.append(SA_Being.best_distance)

    return (progress, SA_Being.best_route,  SA_Being.best_distance)


if __name__ == "__main__":
    points = generate_form_points(10, "square")
    data_model = create_data_model(points)
    solution = GA_implemented(data_model,num_generations=30)
    print_route(solution[1])
    plot_locations_with_connections(data_model["locations"], solution[1])
    input("Press Enter to exit...\n")