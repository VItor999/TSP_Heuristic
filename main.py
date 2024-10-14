from GA_implemented import GA_implemented
from benchmark import benchmark, print_solution , find_route
from tsp_utils.general import *
import argparse  

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
    
    print("################# Custom GA Solution #################")
    solution_GA = GA_implemented(data_model,num_generations=500)
    print(f"Distance: {solution_GA[2]:.2f}  m\n")
    print_route(solution_GA[1])
    plot_locations_with_connections(data_model["locations"], solution_GA[1], "Solution found using custom GA")
    input("Press Enter to exit...\n")