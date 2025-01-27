import json

counter = 0

with open('checker.json', 'r') as file:
    data = json.load(file)
    #print(data)
    print(data[0]['steps']['button'])
    for item in data[0]['steps']:
        counter += 1
    print(counter)