wins = []
num_wins = 0
for x in range(int(input())):
    user_input = input().split()
    if user_input[1] == "win":
        wins.append(user_input[0])
        num_wins += 1
print(wins)
print(num_wins)