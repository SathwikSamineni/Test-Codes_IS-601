text = "(+ (+ 1 2) (+ (+ 3 F) 5))"

class ParserException(Exception):
    pass

def find_open_parenthesis(text):
    """Finds the first open parenthesis and returns the text after it."""
    for index, character in enumerate(text):
        if character == '(':
            return text[index + 1:]
    raise ParserException("Unable to find opening parenthesis")

def get_argument(text):
    """Retrieves the next argument from the text, which can be an integer or a nested operation."""
    start_index = None
    for index, character in enumerate(text):
        if character == '(':
            arg, remaining_text = perform_operation(text[index + 1:])
            return arg, remaining_text
        elif character != ' ' and start_index is None:
            start_index = index
        elif (character == ' ' or character == ')') and start_index is not None:
            
            arg_str = text[start_index:index]
            if not arg_str.isdigit():  
                raise ParserException(f"Invalid argument: {arg_str}")
            arg = int(arg_str)
            remaining_text = text[index + 1:]
            return arg, remaining_text
    raise ParserException("Unable to get argument")

def perform_operation(text):
    """Performs the addition operation on two arguments."""
    if text[0] == '+':
        arg1, remaining_text = get_argument(text[1:])
        arg2, remaining_text = get_argument(remaining_text)
        return arg1 + arg2, remaining_text
    else:
        raise ParserException("Invalid operation")


try:
    result, _ = perform_operation(find_open_parenthesis(text))
    print("Result:", result)
except ParserException as e:
    print("Error:", e)
