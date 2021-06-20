import requests

BASE = "http://127.0.0.1:5000/"

data = [
        {"likes": 44, "name": "rohit", "views": 4634},
        {"likes": 10, "name": "mohit", "views": 874368756},
        {"likes": 98, "name": "leena", "views": 987345}
]

for i in range(len(data)):
    response = requests.put(BASE+ "video/" + str(i), data[i])
    print(response.json())

# response = requests.delete(BASE+ "video/0")
# print(response)
input()
response = requests.patch(BASE+ "video/2", {"views": 99, 'name': 'leenas'})
print(response.json())
input()
response = requests.get(BASE+ "video/2")
print(response.json())