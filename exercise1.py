import sys

def check_input():
    correct_phrase = "Hello world"
    attempts = 4
    
    inputs = sys.stdin.read().splitlines()
    
    for attempt in range(attempts):
        if attempt < len(inputs):  
            user_input = inputs[attempt]
        else:
            break  
        
        if user_input == correct_phrase:
            print("Good job")
            return  
        
        if attempt < attempts - 1:
            print("Please try again")
    
    print("Attempts exceeded")  


check_input()
