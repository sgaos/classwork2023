import requests

server = "http://127.0.0.1:5000"
patient = {"patient_mrn": 12, "attending_email": "shanshan.gao@duke.edu",
           "patient_age": 12}
r = requests.post(server + "/patient/new_patient", json=patient)
print(r.status_code)
print(r.text)

patient = {"patient_mrn": "abd", "attending_email": "shanshan.gao@duke.edu",
           "patient_age": 12}
r = requests.post(server + "/patient/new_patient", json=patient)
print(r.status_code)
print(r.text)

patient = {"patient_mrn": 12, "attending_email": 12,
           "patient_age": "abc"}
r = requests.post(server + "/patient/new_patient", json=patient)
print(r.status_code)
print(r.text)

patient = {"patient_mrn": 12, "attending_email": "shanshan.gao@duke.edu",
           "patient_age": "12"}
r = requests.post(server + "/patient/new_patient", json=patient)
print(r.status_code)
print(r.text)
