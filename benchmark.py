import math
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import matplotlib.pyplot as plt

# This heavlly based on the one available at https://developers.google.com/optimization/routing/tsp
# We intentionally modified it the least possible in order to compare the results obtained by the group
# with a standard solution that anyone can have access and is easy to use without know what is "under the hood";

def plot_locations_with_connections(data, connections):
    """Plots the locations and connections on a 2D plane."""
    locations = data["locations"]
    x_coords, y_coords = zip(*locations)
    
    # Plot the locations
    plt.figure(figsize=(8, 6))
    plt.scatter(x_coords, y_coords, c="blue", marker="o", s=100)
    
    # Annotate each point with its index
    for i, (x, y) in enumerate(locations):
        plt.text(x, y, f'{i}', fontsize=12, ha='right')

    # Draw the connections
    for i in range(len(connections) - 1):
        start_index = connections[i]
        end_index = connections[i + 1]
        plt.plot(
            [locations[start_index][0], locations[end_index][0]], 
            [locations[start_index][1], locations[end_index][1]], 
            "r-"
        )

    plt.xlabel("X Coordinates")
    plt.ylabel("Y Coordinates")
    plt.title("Locations with Connections")
    plt.grid(True)
    plt.show()



def create_data_model():
    """Stores the data for the problem."""
    data = {}
    # Locations in block units
    data["locations"] = [
       (80, 324), (412, 424), (574, 634), (650, 782), (788, 960),
       (960, 460), (66, 456), (900, 966), (762, 54), (942, 156), 
       (964, 732),  # official ones
       #mais 20 
       #(690, 578), (556, 833), (736, 195), (364, 847), (836, 677), 
       # (969, 197), (627, 431), (171, 284), (211, 374), (528, 494),
#
       # #mais 40
       # (515, 565), (317, 418), (487, 372), (74, 203), (750, 811),
       # (442, 423), (902, 582), (320, 569), (119, 922), (396, 121),
       # (222, 70), (433, 112), (827, 234), (345, 828), (253, 439),
       # (743, 476), (132, 153), (933, 185), (622, 458), (217, 960),
#
       # #mais 50
       # (461, 959), (884, 106), (72, 510), (640, 624), (901, 414),
       # (510, 315), (895, 647), (588, 438), (547, 67), (413, 391),
       # (153, 392), (798, 795), (842, 737), (553, 54), (766, 773),
       # (737, 472), (770, 363), (229, 828), (883, 859), (704, 138),
       # (628, 70), (521, 899), (569, 797), (722, 168), (806, 559),
       # (528, 199), (652, 932), (308, 554), (352, 322), (357, 80),
       # (531, 623), (362, 966), (152, 531), (387, 202), (284, 966),
       # (575, 439), (292, 491), (208, 376), (916, 924), (840, 496),
       # (696, 131), (719, 84), (486, 501), (105, 684), (204, 50),
       # (537, 644), (496, 449), (233, 219), (734, 744), (495, 588)
       ]
    data["num_vehicles"] = 1
    data["depot"] = 0
    return data


def compute_euclidean_distance_matrix(locations):
    """Creates callback to return distance between points."""
    distances = {}
    for from_counter, from_node in enumerate(locations):
        distances[from_counter] = {}
        for to_counter, to_node in enumerate(locations):
            if from_counter == to_counter:
                distances[from_counter][to_counter] = 0
            else:
                # Euclidean distance
                distances[from_counter][to_counter] = int(
                    math.hypot((from_node[0] - to_node[0]), (from_node[1] - to_node[1]))
                )
    return distances


def print_solution(manager, routing, solution):
    """Prints solution on console."""
    print(f"Objective: {solution.ObjectiveValue()}")
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
        if(not routing.IsEnd(index)):
            route.append(index)
    index = routing.Start(0)
    route.append(index)
    plan_output += f" {manager.IndexToNode(index)}\n"
    print(plan_output)
    plan_output += f"Objective: {route_distance}m\n"
    return route

def benchmark():
    """Entry point of the program."""
    # Instantiate the data problem.
    data = create_data_model()

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(
        len(data["locations"]), data["num_vehicles"], data["depot"]
    )

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)

    distance_matrix = compute_euclidean_distance_matrix(data["locations"])

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

    # Print solution on console.
    if solution:
        route = print_solution(manager, routing, solution)
        plot_locations_with_connections(data, route)

if __name__ == "__main__":
    benchmark()