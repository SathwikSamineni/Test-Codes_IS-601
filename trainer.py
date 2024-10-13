class Trainer():
    def __init__(self, name, health) ->  None:
        self.name = name
        self.health = health
    def print_info(self):
        print(f"My Name is: {self.name}, and I have Health: {self.health}")

ash = Trainer("Ash", 100)
ash.print_info()   
        
        

