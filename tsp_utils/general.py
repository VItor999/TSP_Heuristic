import math
import random
import matplotlib.pyplot as plt

def create_data_model(locations = None):
    """Stores the data for the problem."""
    data = {}
    # If no custom locations provided used the fixed one 
    if(locations == None):
        data["locations"] = [
        (80, 324), (412, 424), (574, 634), (650, 782), (788, 960),
        (960, 460), (66, 456), (900, 966), (762, 54), (942, 156), 
        (964, 732), 
        ]
    else:
        data["locations"] = locations
    data["salesman"] = 1
    data["depot"] = 0
    return data

def plot_points(points, title = ""):
    x_values = [p[0] for p in points]
    y_values = [p[1] for p in points]

    plt.figure(figsize=(6, 6))
    plt.scatter(x_values, y_values, color='blue', s=100)  # Scatter plot for points

    # Label each point with its index
    for i, (x, y) in enumerate(points):
        plt.text(x, y, str(i), fontsize=12, ha='right', color='red')

    # Set the grid size and limits
    plt.xlim(0, 1000)
    plt.ylim(0, 1000)

    plt.title(title)
    plt.grid(True)
    plt.show()
    
def generate_form_points(num_points, shape='square'):
    '''
    Generates points for a given shape inside a 1000x1000 grid with a 100-point margin.

    :param num_points: The number of points to generate.
    :type num_points: int
    :param shape:  The shape to generate points for. Can be 'circle', 'triangle', 'square', or 'hexagon'. Defaults to 'square'
    :type shape: str, optional
    :raises ValueError: A circle requires at least 8 points 
    :raises ValueError: A square requires at least 4 points 
    :raises ValueError: A triangle requires at least 3 points
    :raises ValueError: A hexagon requires at least 6 points
    :return: points generated 
    :rtype: list[tuple(int, int)]
    '''
    if shape == "circle" and num_points < 8:
        raise ValueError("A circle requires at least 8 points.")
    elif shape == "square" and num_points < 4:
        raise ValueError("A square requires at least 4 points.")
    elif shape == "triangle" and num_points < 3:
        raise ValueError("A triangle requires at least 3 points.")
    elif shape == "hexagon" and num_points < 6:
        raise ValueError("A hexagon requires at least 6 points.")
    shape = shape.lower()
    grid_size = 1000
    margin = 100
    center_x = grid_size / 2
    center_y = grid_size / 2

    if shape == "circle":
        radius = (grid_size - 2 * margin) / 2  # Maximum radius that fits within the grid
        points = []
        
        for i in range(num_points): 
            angle = 2 * math.pi * i / num_points
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            points.append((x, y))
    
    elif shape == "square":
        side_length = grid_size - 2 * margin
        vertices = [
            (center_x - side_length / 2, center_y - side_length / 2),  # Bottom-left
            (center_x + side_length / 2, center_y - side_length / 2),  # Bottom-right
            (center_x + side_length / 2, center_y + side_length / 2),  # Top-right
            (center_x - side_length / 2, center_y + side_length / 2)   # Top-left
        ]
        points = []
        points_per_edge = num_points // 4

        for i in range(4):
            start_vertex = vertices[i]
            end_vertex = vertices[(i + 1) % 4]
            
            for j in range(points_per_edge):
                t = j / (points_per_edge)
                x = int((1 - t) * start_vertex[0] + t * end_vertex[0])
                y = int((1 - t) * start_vertex[1] + t * end_vertex[1])
                points.append((x, y))

    elif shape == "hexagon":
        radius = (grid_size - 2 * margin) / 2  # Radius based on grid size and margin
        vertices = []
        for i in range(6):
            angle_deg = 60 * i  # 60 degrees between each vertex
            angle_rad = math.radians(angle_deg)
            x = int(center_x + radius * math.cos(angle_rad))
            y = int(center_y + radius * math.sin(angle_rad))
            vertices.append((x, y))

        # Distribute points along the edges of the hexagon
        points = []
        points_per_edge = num_points // 6  # Number of points per edge

        for i in range(6):
            start_vertex = vertices[i]
            end_vertex = vertices[(i + 1) % 6]

            # Generate points along each edge
            for j in range(points_per_edge):
                t = j / (points_per_edge - 1)  # Parameter t ranges from 0 to 1
                x = int((1 - t) * start_vertex[0] + t * end_vertex[0])
                y = int((1 - t) * start_vertex[1] + t * end_vertex[1])
                points.append((x, y))
    
    else: ##triangle
        side_length = (grid_size - 2 * margin) * math.sqrt(3) / 3  # Side length of equilateral triangle
        vertices = [
            (center_x, center_y + side_length / math.sqrt(3)),  # Top vertex
            (center_x - side_length / 2, center_y - side_length / (2 * math.sqrt(3))),  # Bottom-left vertex
            (center_x + side_length / 2, center_y - side_length / (2 * math.sqrt(3)))  # Bottom-right vertex
        ]
        points = []
        points_per_edge = num_points // 3

        for i in range(3):
            start_vertex = vertices[i]
            end_vertex = vertices[(i + 1) % 3]
            
            for j in range(points_per_edge):
                t = j / (points_per_edge - 1)
                x = (1 - t) * start_vertex[0] + t * end_vertex[0]
                y = (1 - t) * start_vertex[1] + t * end_vertex[1]
                points.append((x, y))
    return points


def parse_input(filename = "teste1.txt"):
    '''
    Reads X and Y coordinates from a file and returns a list of (x, y) tuples. The file must contains the X and Y coordinates in deferent lines

    :param filename: Filename, defaults to "teste1.txt"
    :type filename: str, optional
    :return: list of (x, y) tuples with the data read
    :rtype: list[tuple(int, int)]
    '''
 
    with open(filename, 'r') as file:
        lines = file.readlines()

    # Strip any extra spaces or newline characters
    x_values = list(map(int, lines[0].strip().split()))
    y_values = list(map(int, lines[1].strip().split()))
    
    if(x_values != y_values):
        raise ValueError("Invalid data set")
    # Pair X and Y values into tuples
    locations = list(zip(x_values, y_values))

    return locations
    

def plot_locations_with_connections(locations, connections, title = "Empty Title"):
    '''
    This function will generate the graph of the calculated route

    :param locations: list of tuples will the locations off all the points of the route 
    :type locations: list[tuple(int, int)]
    :param connections: list with the connections between points
    :type connections: list[int]
    :param title: title of th graph, default to "Empty title"
    :type title: str
    '''
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
    plt.title(title)
    plt.grid(True)
    plt.show(block=False)
    

def compute_euclidean_distance_matrix(locations, print_matrix = False):
    '''
    Will return the distance matrix for a set of locations

    :param locations: X and Y locations of a ciy
    :type locations: list[tuple(x,y)]
    :param print_matrix: boolean to print the calculated matrix, defaults to False
    :type print_matrix: bool, optional
    :return: distance matrix 
    :rtype: dict
    '''
    
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
    if (print_matrix):
        print_matrix_form(distances)
    return distances

def print_matrix_form(matrix):
    '''
    Prints in a human readable format the distance matrix 

    :param matrix: matrix with the distance  between all points can be calculated with compute_euclidean_distance_matrix
    :type matrix: dict
    '''
    num_locations = len(matrix)
    
    # Print header row (column labels)
    print("   ", end=" ")
    for i in range(num_locations):
        print(f"{i:5}", end=" ")
    print()
    
    # Print each row of the matrix
    for from_node, row in matrix.items():
        print(f"{from_node:2} ", end=" ")  # Row label (from node)
        for to_node in range(num_locations):
            print(f"{row[to_node]:5}", end=" ")  # Each distance
        print()  # Newline after each row

    """Calculates the total distance for a given route using the provided distance matrix.
    
    Args:
        distance_matrix (dict): The distance matrix as a dictionary of dictionaries.
        route (List[int]): The route represented as a list of node indices (e.g., [0, 1, 3, 0]).
        
    Returns:
        int: Total distance of the route.
    """

def calculate_route_distance(distance_matrix, route):
    '''
    Calculates the total distance for a given route using the provided distance matrix.

    :param distance_matrix: The distance matrix as a dictionary of dictionaries.
    :type distance_matrix: (dict)
    :param route: sequence of cities to visit
    :type route: list[int]
    :return: Total distance
    :rtype: int
    '''
    total_distance = 0

    # Calculate the distance for each step in the route
    for i in range(len(route) - 1):
        from_node = route[i]
        to_node = route[i + 1]
        total_distance += distance_matrix[from_node][to_node]

    return total_distance


def print_route(route):
    '''
    Prints a route 

    :param route: list of sequential cities to visit
    :type route: list(int)
    '''
    for index in range(0,len(route)):
        if index != len(route)-1:
            print(f"{route[index]:2d}", end="->")
        else:
            print(f"{route[index]:2d}")
            
def generate_random_points(num_points = 20):
    '''
    Generates random points with range 0 - 1000

    :param num_points: number of cities to generate, defaults to 20
    :type num_points: int, optional
    :return: list with tuples of the points generated 
    :rtype: list[tuple(int, int)]
    '''
    points = [(random.randint(0, 1000), random.randint(0, 1000)) for _ in range(num_points)]
    return points
            
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
            
if __name__ == "__main__":
    # Generate hexagon points
    points = generate_form_points(4, "square")
    
    compute_euclidean_distance_matrix(points,True)
    # Plot the hexagon points with labels
    plot_points(points,"Cities to visit")
    input("Press Enter to exit...\n")    
   