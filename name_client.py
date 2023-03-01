import requests

server = "http://vcm-21170.vm.duke.edu:5000"

out_data = {"name": "David Ward", "net_id": "daw74",
            "e-mail": "david.a.ward@duke.edu"}
r = requests.post(server + "/student", json=out_data)
print(r.status_code)
print(r.text)

r = requests.get(server + "/list")
print(r.text)
