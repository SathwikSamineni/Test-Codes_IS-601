import sys

def check_input():
    correct_phrase = "Hello world"
    attempts = 4
    
    # Read all input at once and split it into lines
    inputs = sys.stdin.read().splitlines()
    
    for attempt in range(attempts):
        if attempt < len(inputs):  # Check if there are enough inputs provided
            user_input = inputs[attempt]
        else:
            break  # If no input left, exit the loop
        
        if user_input == correct_phrase:
            print("Good job")
            return  # Exit if the correct phrase is entered
        
        if attempt < attempts - 1:
            print("Please try again")
    
    print("Attempts exceeded")  # After all attempts are used and the correct phrase wasn't entered

# Run the function
check_input()
