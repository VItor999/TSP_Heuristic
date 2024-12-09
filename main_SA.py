from algorithms.SA_implemented import simulated_annealing
from benchmark import benchmark, print_solution , find_route
from tsp_utils.general import *
import argparse  

#TODO 
#  - MUST: add here, or in other script a loop to generate the data that will be presented
#   like run 100 for each geometric form and random input with 12 24 36 48 cities 
#   save all this data in a ordered manner. At least save the route, and the distance achieved in 
#   each configuration as well as the answer that the benchmark gave
#   think how we want to display this data 

if __name__ == "__main__":
    # Initialize the argument parser
    parser = argparse.ArgumentParser(description='Benchmark X Genetic Algorithm test')

    # Add arguments for each parameter
    parser.add_argument('--num_cities', type=int, default=20, help='Number of cities')
    parser.add_argument('--population_size', type=int, default=100, help='Population size')
    parser.add_argument('--num_generations', type=int, default=100, help='Number of generations')
    parser.add_argument('--mutation_rate', type=float, default=0.01, help='Mutation rate (0.0 - 1.0)')
    parser.add_argument('--tournament_size', type=int, default=5, help='Tournament size')
    parser.add_argument('--elite_size', type=int, default=5, help='Elite size')
    parser.add_argument('--shape', choices=['square', 'circle', 'hexagon', 'triangle'], 
                        default='square', help='Shape type (square, circle, hexagon, triangle)')
    parser.add_argument('--random', action='store_true', help='Enable random behavior (default is disabled)')
    parser.add_argument('--file', type=str, help='Path to the file to open')
    

    # Parse the arguments
    args = parser.parse_args()
    num_cities = args.num_cities
    if args.file != None :
        cities = parse_input(args.file)
    elif args.random:
        cities = generate_random_points(num_cities)
    else:
        cities = generate_form_points(num_cities, args.shape)
    
    data_model = create_data_model(cities)
    
    print("################# Benchmark Solution #################")
    solution_benchmark = benchmark(data_model["locations"])
    print_solution(solution_benchmark[0], solution_benchmark[1], solution_benchmark[2])
    route = find_route(solution_benchmark[1], solution_benchmark[2])
    plot_locations_with_connections(solution_benchmark[3]["locations"], route, "Solution found using benchmark")
    
    print("################# Custom SA Solution #################")
    distance_matrix = compute_euclidean_distance_matrix(data_model["locations"])
    initial_temperature = 10000000
    cooling_rate = 1
    min_temperature = 1
    best_route, best_distance = simulated_annealing(distance_matrix, initial_temperature, cooling_rate, min_temperature, 20)
    print(f"Distance: {best_distance:.2f}  m\n")
    print_route(best_route)
    plot_locations_with_connections(data_model["locations"], best_route, "Solution found using custom SA")
    input("Press Enter to exit...\n")