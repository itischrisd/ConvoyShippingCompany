input_array = []

while True:
    input_string = input()
    if input_string == "MEOW":
        break
    input_array.append(input_string)

max = 0
for input_string in input_array:
    if int(input_string.split().pop(1)) > max:
        name = input_string.split().pop(0)
        max = int(input_string.split().pop(1))

print(name)