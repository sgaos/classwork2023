""""
Database = Dictionary
keys -> ids for the patients
value: int

{ 1: {"id": 1, "name": "David", "blood_type": "O+"},
 2: {"id": 1, "name": "David", "blood_type": "O+"},
 3: {"id": 1, "name": "David", "blood_type": "O+", "tests": []},


"""

from flask import Flask, request, jsonify

db = {}

app = Flask(__name__)

def add_patient_to_db(id, name, blood_type):
    new_patient = {"id": id,
                   "name": name,
                   "blood_type": blood_type }
    db[id] = new_patient
    print(db)


@app.route("/new_patient", methods=["POST"])
def post_new_patient():
    # Get input data
    in_data = request.get_json()
    # Call other functions to do the work
    answer, status_code = new_patient_driver(in_data)
    # Return a response
    return jsonify(answer), status_code


def new_patient_driver(in_data):
    # Validate input
    validation = validate_input_data(in_data)
    if validation is not True:
        return validation, 400
    # Do the work
    add_patient_to_db(in_data["id"], in_data["name"], in_data["blood_type"])
    # Return an answer
    return "Patient successfully added", 200

def validate_input_data(in_data):
    if type(in_data) is not dict:
        return "Input is not a dictionary"
    expected_keys = ["name", "id", "blood_type"]
    expected_types = [str, int, str]
    for key, value_type in zip(expected_keys, expected_types):
        if key not in in_data:
            return "Key {} is missing from input".format(key)
        if type(in_data[key]) is not value_type:
            return "Key {} has the incorrect value type".format(key)
    return True


if __name__ == '__main__':
    app.run()
