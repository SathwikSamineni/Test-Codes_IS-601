def check_input():
    correct_phrase = "Hello world"
    attempts = 4
    
    for attempt in range(attempts):
        user_input = input()  # No prompt, as your test cases expect direct input
        
        if user_input == correct_phrase:
            print("Good job")
            return  # Exit if the correct phrase is entered
        
        if attempt < attempts - 1:
            print("Please try again")
    
    print("Attempts exceeded")  # After all attempts are used and the correct phrase wasn't entered

# Run the function
check_input()
