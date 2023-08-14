import logging
from flask import Flask, request, jsonify
from datetime import datetime

db = {}  # global dictionary
app = Flask(__name__)  # instance of Flask


def add_new_patient(patient_mrn, attending_email,
                    patient_age):
    """
    This function adds patient information includes patient mrn,
    attending_email and patient age to
    database
    :param patient_mrn: (str/int)
    the unique medical
    record number for the patient
    :param attending_email: (str) string containing an e-mail address
    :param patient_age:  (str/ int)
    patient's age in years
    :return: None
    """
    request_result = []
    new_patient = {"patient_mrn": patient_mrn,
                   "attending_email": attending_email,
                   "patient_age": patient_age,
                   "tests":
                       dict(HR=dict(test_name="HR", test_result=[],
                                    status_string=[], requests=request_result),
                            HDL=dict(test_name="HDL", test_result=[],
                                     status_string=[],
                                     requests=request_result),
                            LDL=dict(test_name="LDL", test_result=[],
                                     status_string=[],
                                     requests=request_result),
                            TSH=dict(test_name="TSH", test_result=[],
                                     status_string=[],
                                     requests=request_result))}

    db[patient_mrn] = new_patient
    logging.info("Patients(mrn {}) information should send to {} was added".
                 format(patient_mrn, attending_email))


@app.route("/patient/new_patient", methods=["POST"])
def post_new_patient():
    """
    Post route to receive information about
    a new patient and validate the input
    information type and allows information
    about a new patient to be added to the server.
    return: (str)a message with information about
    failure or success of operation
    and (int) status code
    """
    # get input data
    in_data = request.get_json()
    # call function do the work
    answer, status_code = new_patient_driver(in_data)
    patient_mrn = str(in_data["patient_mrn"])
    attending_email = str(in_data["attending_email"])
    if status_code == 200:
        logging.info("Patients(mrn {}) information should send to "
                     "{} was added".format(patient_mrn, attending_email))
    # return a response
    return jsonify(answer), status_code


def new_patient_driver(in_data):
    """
    This funtion performs the data validation and allows information
    about a new patient to be added to the server for the "/new_patient" route
    by calling validation and implementation function
    :param in_data: (dict) Data received from the POST request
    :return: (str)a message with information about failure
    or success of operation and (int) status code
    """
    validation_keys = validate_input_data_keys_new_patient(in_data)
    # validation fail
    if validation_keys is not True:
        return validation_keys, 400
    validation_type = validate_in_data_type(in_data)
    if validation_type is not True:
        return validation_type, 400
    # validation pass
    add_new_patient(int(in_data["patient_mrn"]), in_data["attending_email"],
                    int(in_data["patient_age"]))
    return "Patient successfully added", 200


def validate_input_data_keys_new_patient(in_data):
    """
    The function validates the keys of input data for "/new_patient" route
    :param in_data: (dict)Data received from the POST request
    :return: (str)a message says if there is a
    problem of input data or True(boolean) if validation success
    """
    if type(in_data) is not dict:
        return "Input is not dictionary"
    # validate if keys excited
    # create expected keys
    expected_keys = ["patient_mrn", "attending_email", "patient_age"]
    for key in expected_keys:
        if key not in in_data:
            return "key {} is missing from input".format(key)
    return True


def validate_in_data_type(in_data):
    """
    The function validates the type of input data for "/new_patient" route
    :param in_data: (dict) Data received from the POST request
    :return: (str)a message says if there is a
    problem of input data or True(boolean) if operation success
    """
    try:
        int(in_data["patient_mrn"])
    except ValueError:
        return "Patient_mrn should be an integer"
    try:
        int(in_data["patient_age"])
    except ValueError:
        return "patient_age should be an integer"

    if not isinstance(in_data["attending_email"], str):
        return "attending_email should be a a string"
    return True
