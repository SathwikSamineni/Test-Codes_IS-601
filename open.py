file_object = open('workfile.txt', 'r')
print(file_object.read()) 
file_object.close()

file_object = open('workfile.txt', 'r')
print(file_object.read(10)) 
file_object.close()

file_object = open('workfile.txt', 'r')
print(file_object.readline()) 
file_object.close()

file_object = open('workfile.txt', 'r')
for line in file_object: 
    print(line)
file_object.close()