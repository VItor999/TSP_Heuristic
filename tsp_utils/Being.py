# TODO list 
# MUST fix documentation
# MUST add method to save data and route (save data)
# MUST rethink how the mutation is being incremented

class Being:
    static_ID = 0
    def __init__(self, route, parentsID=[0, 0], mutation_number=0, born_on=0, fitness = 0):
        self.route = route 
        self.parentsID = parentsID
        self.born_on = born_on
        self.mutation_number = mutation_number
        self.fitness = fitness
        Being.static_ID += 1
        self.id = Being.static_ID
        
    
    def get_info(self):
        """Method to return a summary of the being's properties."""
        return {
            'route': self.route,
            'parentsID': self.parentsID,
            'mutation_number': self.mutation_number,
            'born_on': self.born_on,
            'fitness': self.fitness,
            'distance': 1/self.fitness,
            'id': self.id
        }
    
    def update_mutation_number(self, number_of_new_mutations=1):
        self.mutation_number += number_of_new_mutations

    def set_route(self, new_route):
        self.route = new_route

    @staticmethod
    def reset_ids():
        Being.static_ID = 0
        
    def __str__(self):
        """String representation of the Being."""
        return f"Being {self.id} born_on {self.born_on} with a total of {self.mutation_number} mutations. Originated from {self.parentsID}. \n\t {self.route})"