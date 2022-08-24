# write your code here
with open("salary.txt", "r") as input, open("salary_year.txt", "w") as output:
    for line in input:
        output.write(str(int(line.rstrip("\n")) * 12) + "\n")