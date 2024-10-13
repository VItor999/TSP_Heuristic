from GA_implemented import GA_implemented
from benchmark import benchmark, print_solution , find_route
from tsp_utils.general import *

if __name__ == "__main__":
    #points = generate_form_points(50, "hexagon")
    points = generate_random_points(50)
    data_model = create_data_model(points)
    num_cities = len(data_model["locations"])
    
    print("################# Benchmark Solution #################")
    solution_benchmark = benchmark(data_model["locations"])
    print_solution(solution_benchmark[0], solution_benchmark[1], solution_benchmark[2])
    route = find_route(solution_benchmark[1], solution_benchmark[2])
    plot_locations_with_connections(solution_benchmark[3]["locations"], route, "Solution found using benchmark")
    
    print("################# Custom GA Solution #################")
    solution_GA = GA_implemented(data_model,num_generations=500)
    print(f"Distance: {solution_GA[2]:.2f}\n")
    print_route(solution_GA[1])
    plot_locations_with_connections(data_model["locations"], solution_GA[1], "Solution found using custom GA")
    input("Press Enter to exit...\n")