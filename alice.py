class ParserException(Exception):
    pass

def find_open_parenthesis(text):
    for index, character in enumerate(text):
        if character == '(':
            return text[index + 1:]
    raise ParserException("Unable to find opening parenthesis")

def get_argument(text):
    start_index = None
    for index, character in enumerate(text):
        if character == '(':
            # Recursively parse nested addition expressions
            arg, remaining_text = perform_operation(text[index + 1:])
            return arg, remaining_text
        elif character != ' ' and start_index is None:
            start_index = index
        elif (character == ' ' or character == ')') and start_index is not None:
            try:
                # Parse integer argument
                arg = int(text[start_index:index])
                remaining_text = text[index + 1:]
                return arg, remaining_text
            except ValueError:
                raise ParserException(f"Invalid argument: {text[start_index:index]}")
    raise ParserException("Unable to get argument")

def perform_operation(text):
    if text[0] == '+':
        # Parse two arguments and add them
        arg1, remaining_text = get_argument(text[1:])
        arg2, remaining_text = get_argument(remaining_text)
        return arg1 + arg2, remaining_text
    else:
        raise ParserException("Invalid operation")

# Example usage:
try:
    expression = "(+ (+ 1 2) (+ (+ 3 F) 5))"
    result, _ = perform_operation(find_open_parenthesis(expression))
    print("Result:", result)
except ParserException as e:
    print("Error:", e)
