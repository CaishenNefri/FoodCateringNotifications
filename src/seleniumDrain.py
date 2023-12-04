import requests
import json
response = requests.get("http://localhost:4444/wd/hub/status")
loaded = json.loads(response.text)
node_id = loaded["value"]["nodes"][0]["id"]

requests.post(f"http://localhost:4444/se/grid/distributor/node/{node_id}/drain", headers={"X-REGISTRATION-SECRET": ""})

# import requests

# url = 'https://www.w3schools.com/python/demopage.js'

# x = requests.get(url)

# print(x.json())

# print(x.firstname)

