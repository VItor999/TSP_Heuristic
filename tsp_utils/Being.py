class Being:
    static_ID = 0
    
    def __init__(self, route, parentsID=[0, 0], mutation_number=0, born_on=0, fitness=0):
        """
        Initializes a new Being instance.
        
        :param route: The path or sequence of cities (list[int])
        :param parentsID: List of two IDs representing the parents (list[int], optional)
        :param mutation_number: Count of mutations for this being (int, optional)
        :param born_on: The generation when this being was created (int, optional)
        :param fitness: The fitness score of this being, where higher is better (float, optional)
        """
        self.route = route
        self.parentsID = parentsID
        self.born_on = born_on
        self.mutation_number = mutation_number
        self.fitness = fitness
        self.mutation_type=[]
        Being.static_ID += 1
        self.id = Being.static_ID
        
    def get_info(self):
        """
        Returns a summary of the being's properties in a dictionary format.
        
        :return: A dictionary with keys 'route', 'parentsID', 'mutation_number', 'mutation_type', 'born_on', 'fitness', 'distance', 'id'
        :rtype: dict
        """
        return {
            'route': self.route,
            'parentsID': self.parentsID,
            'mutation_number': self.mutation_number,
            'mutation_type': self.mutation_type,
            'born_on': self.born_on,
            'fitness': self.fitness,
            'distance': 1/self.fitness if self.fitness != 0 else float('inf'),
            'id': self.id
        }

    
    def update_mutation_number(self, number_of_new_mutations=1, mutation_type=None):
        """
        Increments the mutation number and tracks the type of mutation if provided.
        
        :param number_of_new_mutations: Number of new mutations to add (int, optional)
        :param mutation_type: A string representing the type of mutation (str, optional)
        """
        self.mutation_number += number_of_new_mutations
        self.mutation_type.append(mutation_type)


    def set_route(self, new_route):
        """
        Sets a new route for the being.
        
        :param new_route: A list representing the new route
        """
        self.route = new_route

    @staticmethod
    def reset_ids():
        """
        Resets the static ID counter to 0.
        """
        Being.static_ID = 0
        
    def __str__(self):
        """
        Returns a string representation of the Being instance.
        
        :return: A string summarizing the being
        """
        aux_str = ""
        if(self.mutation_number !=0):
            aux_str = f"Was suffered mutation of type: {self.mutation_type}"
            
        else :
            aux_str = "Hasn't suffered mutation"
        return (f"Being {self.id} born_on {self.born_on}." + aux_str + 
                f"Originated from {self.parentsID}. \n\t {self.route})")
