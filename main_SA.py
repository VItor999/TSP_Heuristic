from SA_implemented import SA_implemented
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
    parser = argparse.ArgumentParser(description='Benchmark X Simulated Annealing test')

    # Add arguments for each parameter
    parser.add_argument('--num_cities', type=int, default=20, help='Number of cities')
    parser.add_argument('--movement_percentage', type=float, default=0.15, help='mu value')
    parser.add_argument('--worse_solutions', type=float, default=0.05, help='phi value')
    parser.add_argument('--rho', type=float, default=1.0, help='rho value')
    parser.add_argument('--beta', type=float, default=0.8, help='beta value')
    parser.add_argument('--reduction_number', type=int, default=20, help='How many stages of temperature')
    parser.add_argument('--cooling_is_constant', type=bool, default=True, help='Define cooling function')
    parser.add_argument('--delta', type=float, default=0.1, help='delta value')
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
    solution_SA = SA_implemented(data_model,movement_percentage = 0.20, worse_solutions = 0.05, rho = 5,
                   beta = 0.6, reduction_number = 100,cooling_is_constant=True,delta=0.1)
    print(f"Distance: {solution_SA[2]:.2f}  m\n")
    print_route(solution_SA[1])
    plot_locations_with_connections(data_model["locations"], solution_SA[1], "Solution found using custom SA")
    input("Press Enter to exit...\n")