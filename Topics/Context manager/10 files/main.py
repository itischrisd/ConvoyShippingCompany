# write your code here
for i in range(10):
    with open("file" + str(i + 1) + ".txt", "w") as file:
        file.write(str(i + 1))