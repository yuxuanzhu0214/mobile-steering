import requests
import time

url = 'http://127.0.0.1:3000/car'
carData = {
    "rpm": 1300,
    "gear": 2,
    "speed": 100,
}

print("Generating workloads to dashboard server...")
while True:
    carData["rpm"] += 20
    carData["rpm"] %= 8000
    carData["speed"] += 1
    carData["speed"] %= 220
    requests.post(url, json = carData)
