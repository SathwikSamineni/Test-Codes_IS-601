import operator

user_input = input("equation: ")

action_map = {
    "+": operator.__eq__
}
data = user_input.split(" ")

answer = action_map[data[1]](data[0], data[1])
print(f'answer is {answer}')

