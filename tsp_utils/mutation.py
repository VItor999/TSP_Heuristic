import random

# Swap Mutation
def swap_mutation(route):
    num_cities = len(route)
    city1 = random.randint(0, num_cities - 1)
    city2 = random.randint(0, num_cities - 1)
    route[city1], route[city2] = route[city2], route[city1]
    return route

# Inversion Mutation
def inversion_mutation(route):
    start, end = sorted([random.randint(0, len(route)-1) for _ in range(2)])
    route[start:end] = route[start:end][::-1]
    return route

# Scramble Mutation
def scramble_mutation(route):
    start, end = sorted([random.randint(0, len(route)-1) for _ in range(2)])
    subset = route[start:end]
    random.shuffle(subset)
    route[start:end] = subset
    return route

# Displacement Mutation
def displacement_mutation(route):
    start, end = sorted([random.randint(0, len(route)-1) for _ in range(2)])
    segment = route[start:end]
    del route[start:end]
    insert_at = random.randint(0, len(route)-1)
    route[insert_at:insert_at] = segment
    return route