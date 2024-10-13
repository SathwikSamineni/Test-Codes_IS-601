import json
class Exercise3:
    def __init__(self, file_name):
        with open(file_name, 'r') as file:
            self.data = json.load(file)
    
    def get_username(self):
        return self.data.get('username', '')
    
    def get_time_remaining(self):
        return self.data.get('time_remaining', 0)
    
    def add_hour(self):
        self.data['time_remaining'] += 60
    
    def get_items(self):
        return list(self.data.get('shopping_cart', {}).keys())
    
    def get_total(self):
        return sum(self.data.get('shopping_cart', {}).values())

# Example usage
if __name__ == "__main__":
    # Instantiate the class with the example file
    exercise = Exercise3('exercise_3/example.json')
    
    # Demonstrate method usage
    print("Username:", exercise.get_username())
    print("Time Remaining:", exercise.get_time_remaining())
    print("Items in cart:", exercise.get_items())
    print("Total cost of items:", exercise.get_total())
    
    # Adding one hour
    exercise.add_hour()
    print("Time Remaining after adding an hour:", exercise.get_time_remaining())
