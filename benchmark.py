from tsp_utils.general import *
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

# This heavily based on the one available at https://developers.google.com/optimization/routing/tsp
# We intentionally modified it the least possible in order to compare the results obtained by the group
# with a standard solution that anyone can have access and is easy to use without know what is "under the hood";

def find_route(routing, solution):  
    '''
    Prints benchmark solution
    :param routing: solution routing
    :type routing: RoutingModel
    :param solution: solution data
    :type solution: Assignment
    :return: None
    :rtype: _type_
    '''
    index = routing.Start(0)
    route = list()
    route.append(index)
    while not routing.IsEnd(index):
        previous_index = index
        index = solution.Value(routing.NextVar(index))
        if(not routing.IsEnd(index)):
            route.append(index)
    index = routing.Start(0)
    route.append(index)
    return route

def print_solution(manager, routing, solution):
    '''
    Prints benchmark solution
    :param manager: solution manager
    :type manager: RoutingIndexManager
    :param routing: solution routing
    :type routing: RoutingModel
    :param solution: solution data
    :type solution: Assignment
    :return: None
    :rtype: _type_
    '''
    print(f"Objective: {solution.ObjectiveValue()} m")
    index = routing.Start(0)
    plan_output = "Route:\n"
    route_distance = 0
    route = list()
    route.append(index)
    while not routing.IsEnd(index):
        plan_output += f" {manager.IndexToNode(index)} ->"
        previous_index = index
        index = solution.Value(routing.NextVar(index))
        route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
    index = routing.Start(0)
    plan_output += f" {manager.IndexToNode(index)}\n"
    print(plan_output)

def benchmark(locations = None, points_num = 4, shape = 'square'):
    '''
    Solves the problem using the default/ out of the box  solution form google OR

    :param points: set of points to be used, defaults to None
    :type points: list of (x,y) tuples, optional
    :param points_num: number of points to generate, defaults to 10
    :type points_num: int, optional
    :param shape: string the defines the shape to be generated, defaults to square
    :type shape: str, optional
    :return: solution found, else None
    :rtype: (RoutingIndexManager, RoutingModel, Assignment, data_model_model) objects from google OR and custom data_model_model
    '''
    # Instantiate the data_model problem.
    if(locations == None):
        locations = generate_form_points(points_num, shape)
        
    data_model = create_data_model(locations)

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(
        len(data_model["locations"]), data_model["salesman"], data_model["depot"]
    )

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)

    distance_matrix = compute_euclidean_distance_matrix(data_model["locations"])

    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return distance_matrix[from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    )

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)
    return (manager, routing, solution, data_model) if solution else None

if __name__ == "__main__":
    solution = benchmark(points_num = 20, shape = 'square')
    print_solution(solution[0], solution[1], solution[2])
    route = find_route(solution[1], solution[2])
    plot_locations_with_connections(solution[3]["locations"], route)
    input("Press Enter to exit...\n")