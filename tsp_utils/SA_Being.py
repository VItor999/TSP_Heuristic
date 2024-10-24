class SA_Being:
    static_ID = 0
    
    def __init__(self,current_route,best_route,temperature,distance,best_distance,transitions):
        """
        Initializes a new Being instance.
        
        :param route: The path or sequence of cities (list[int])
        :param parentsID: List of two IDs representing the parents (list[int], optional)
        :param mutation_number: Count of mutations for this being (int, optional)
        :param born_on: The generation when this being was created (int, optional)
        :param fitness: The fitness score of this being, where higher is better (float, optional)
        """
        self.current_route = current_route
        self.best_route = best_route
        self.temperature = temperature
        self.transitions = transitions
        self.distance = distance
        self.best_distance = best_distance
        SA_Being.static_ID += 1
        self.id = SA_Being.static_ID
        
    def get_info(self):
        """
        Returns a summary of the being's properties in a dictionary format.
        
        :return: A dictionary with keys 'current_route', 'best_route', 'temperature', 'distance', 'id'
        :rtype: dict
        """
        return {
            'current_route': self.current_route,
            'best_route': self.best_route,
            'temperature': self.temperature,
            'transitions': self.transitions,
            'distance': self.distance,
            'id': self.id
        }

    
    def update_temperature(self, temperature):
        """
        Updates temperature according to cooling mechanism output
        """
        self.temperature = temperature


    def set_current_route(self, new_route):
        """
        Sets a new route for the being.
        
        :param new_route: A list representing the new route
        """
        self.current_route = new_route

    def set_best_route(self,best_route):
        self.best_route = best_route


    @staticmethod
    def reset_ids():
        """
        Resets the static ID counter to 0.
        """
        SA_Being.static_ID = 0    