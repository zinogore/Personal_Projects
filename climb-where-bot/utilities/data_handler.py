import json

# read database.json
with open("./database.json", "r") as file:
    data = json.load(file)

def get_list_of_gym_names(data=data):
    return [ele["name"] for ele in data["data"]["climbing_gyms"]]