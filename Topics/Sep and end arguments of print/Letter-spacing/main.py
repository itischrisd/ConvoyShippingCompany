input_a = input()
input_b = int(input())
sep=''
for i in range(input_b):
    sep += ' '
print(*list(input_a), sep=sep)