import requests

server = "http://vcm-7631.vm.duke.edu:5002"

r = requests.get(server + "/get_blood_type/M1")
print(r.text)

r = requests.get("https://api.github.com/repos/dward2/BME547/branches")
print(r.text)