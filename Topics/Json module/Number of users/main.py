# write your code here
import json

with open("users.json", "r") as json_file:
    diction = json.load(json_file)
    print(len(diction["users"]))