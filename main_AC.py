from algorithms.AC_implemented import ant_colony
from algorithms.benchmark import benchmark, print_solution , find_route
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
    parser = argparse.ArgumentParser(description='Benchmark X An Colony Optimization test')

    # Add arguments for each parameter
    parser.add_argument('--num_cities', type=int, default=20, help='Number of cities')
    parser.add_argument('--num_generations', type=int, default=350, help='Number of generations')
    parser.add_argument('--alpha', type=float, default=1.5, help='Alpha value')
    parser.add_argument('--beta', type=float, default=3, help='Beta value')
    parser.add_argument('--rho', type=float, default=0.2, help='Rho value')
    parser.add_argument('--q_constant', type=int, default=25000, help='Q value')
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
    

    
    print("################# Custom AC Solution #################")
    AC_solution = ant_colony(data_model, alpha = args.alpha, beta = args.beta, rho = args.rho, q_constant = args.q_constant, generations = args.num_generations)
    AC_best_route = AC_solution[0]
    AC_best_solution_distance = AC_solution[1]
    print(f"Distance: {AC_best_solution_distance:.2f}  m\n")
    print_route(AC_best_route)
    plot_locations_with_connections(data_model["locations"], AC_best_route, "Solution found using AC")

    print("################# Benchmark Solution #################")
    solution_benchmark = benchmark(data_model["locations"])
    print_solution(solution_benchmark[0], solution_benchmark[1], solution_benchmark[2])
    route = find_route(solution_benchmark[1], solution_benchmark[2])
    plot_locations_with_connections(solution_benchmark[3]["locations"], route, "Solution found using benchmark")

    input("Press Enter to exit...\n")