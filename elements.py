a = {
    "name": "bob",
    "something":"fun",
    "age":50,
    "hobbies": {"skiing":True,"snowboarding":True}
}

b = {
    "name": "john",
    "age":24,
    "hobbies":{"knitting":True}
}

value1, value2, value3 = ["item1", "item2", "item3"]

my_list = [name.title() for name in ['billy', 'terrance', 'divesh', 'Monica']]

for i, item in enumerate(my_list):
    print(f"Item number {i} is {item}")

merged_dict = a | b