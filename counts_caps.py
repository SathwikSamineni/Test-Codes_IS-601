def count_caps(sentence):
    if not isinstance(sentence, str):
        return 0

    words = sentence.split()
    capitalized_count = sum(1 for word in words if word[0].isupper())
    
    return capitalized_count

if __name__ == "__main__":
    # Take input from the user
    user_input = input("Enter a sentence: ")
    
    # Count capitalized words in the user-provided sentence
    result = count_caps(user_input)
    
    # Print the result
    print(f"Number of capitalized words: {result}")