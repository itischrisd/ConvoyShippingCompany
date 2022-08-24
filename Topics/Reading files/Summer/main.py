#  write your code here 

text = open("input.txt", "r")
count = 0
for x in text.readlines():
    if x == "summer":
        count += 1
print(x)