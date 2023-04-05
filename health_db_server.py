# health_db_server.py
import logging
import ssl
from flask import Flask, request, jsonify
from pymodm import connect
from PatientModel import Patient
from pymodm import errors as pymodm_errors
from secrets import mongodb_acct, mongodb_pswd
"""
Database has been moved into a MongoDB database
"""

# Create an instance of the Flask server
app = Flask(__name__)


def init_server():
    """ Performs set-up functions before starting server

    This functions performs any needed set-up steps required for server
    operation.  The logging system is configured.  A connection is created
    to the MongoDB database.

    """
    logging.basicConfig(filename="server.log", filemode='w')
    connect("mongodb+srv://{}:{}@bme547.ba348.mongodb.net/"
            "health_db_2023?retryWrites=true&w=majority"
            .format(mongodb_acct, mongodb_pswd), ssl_cert_reqs=ssl.CERT_NONE)


def add_patient_to_db(patient_id, patient_name, blood_type):
    """ Adds a new patient dictionary to the database

    This function receives basic information on a new patient, creates an
    instance of the Patient "MongoModel" class to contain that information,
    and saves this patient information to MongoDB.  The "patient_id" is used
    as the primary key.

    The database is being stored externally to the server in an on-line
    MongoDB database.

    Args:
        patient_id (int): The medical record number of the patient
        patient_name (str): Full name of patient
        blood_type (str): Blood type of the patient

    Returns:
        Patient: a copy of what was saved to the MongoDB database
    """

    new_patient = Patient(patient_id=patient_id,
                          patient_name=patient_name,
                          blood_type=blood_type)
    saved_patient = new_patient.save()
    return saved_patient


def add_test_to_db(patient_id, test_name, test_value):
    """Adds test result for a specific patient.

    This function adds a test result to the specified patient.  First, the
    appropriate patient record is found and downloaded from the MongoDB
    database using the patient_id as the primary key for the search.  Next,
    the "tests" list of the Patient class is updated by appending the new
    test data in the form of a tuple of the test_name and test_value.  The
    updated Patient record is then saved back to MongoDB.

    Args:
        patient_id (int): The medical record number of the patient
        test_name (str): Name of the test to be added
        test_value (int): result of the test

    Returns:
        None
    """
    x = Patient.objects.raw({"_id": patient_id}).first()
    x.tests.append((test_name, test_value))
    x.save()


@app.route("/new_patient", methods=["POST"])
def post_new_patient():
    """POST route to receive information about a new patient and add the
       patient to the database

    This "Flask handler" function receives a POST request to add a new patient
    to the database.  The POST request should receive a dictionary encoded as
    a JSON string in the following format:

        {"id": int,
         "name": str,
         "blood_type": str}

    The value of "id" is an integer that is the medical record number for the
    patient.  The value for "name" is a string that should contain the full
    name of the patient.  The value of "blood_type" is a string that
    contains the blood type of the patient (O+, O-, A+, A-, B+, B-, AB+, AB-).

    The function first receives the dictionary sent with the POST request.  It
    then calls a worker function to act on the data.  It finally returns the
    resulting message and status code.
    """
    # Receive data from POST request
    in_data = request.get_json()
    # Call other functions to do the work
    answer, status_code = new_patient_driver(in_data)
    # Return a response
    return jsonify(answer), status_code


def new_patient_driver(in_data):
    """Implements the '/new_patient' route

    This function performs the data validation and implementation for the
    `/new_patient` route which adds a new patient to the database.  It first
    calls a function that validates that the input data to the route is a
    dictionary that has the necessary keys and value data types.  If the
    necessary information does not exist, the function returns an error message
    and a status code of 400.  Otherwise, another function is called and sent
    the necessary information to add a new patient to the database.  A success
    message and a 200 status code is then returned.

    Args:
        in_data (dict): Data received from the POST request.  Should be a
        dictionary with the format found in the docstring of the
        "post_new_patient" function, but that needs to be verified

    Returns:
        str, int: a message with information about the success or failure of
            the operation and a status code

        """
    # Validate input
    expected_keys = ["name", "id", "blood_type"]
    expected_types = [str, int, str]
    validation = validate_input_data_generic(in_data, expected_keys,
                                             expected_types)
    if validation is not True:
        return validation, 400
    # Do the work
    add_patient_to_db(in_data["id"], in_data["name"], in_data["blood_type"])
    # Return an answer
    return "Patient successfully added", 200


def validate_input_data_generic(in_data, expected_keys, expected_types):
    """Validates that input data is a dictionary with correct information

    This function receives the data that was sent with a POST request.  It
    also receives lists of the keys and value data types that are expected to
    be in this dictionary.  The function first verifies that the data sent to
    the post request is a dictionary.  Then, it verifies that the expected keys
    are found in the dictionary and that the corresponding value data types
    are of the correct type.  An error message is returned if the data is not
    a dictionary, a key is missing or there is an invalid data type.  If keys
    and data types are correct, a value of True is returned.

    Args:
        in_data (dict): object received by the POST request
        expected_keys (list): keys that should be found in the POST request
            dictionary
        expected_types (list): the value data types that should be found in the
            POST request dictionary

    Returns:
        str: error message if there is a problem with the input data, or
        bool: True if input data is valid.

    """
    if type(in_data) is not dict:
        return "Input is not a dictionary"
    for key, value_type in zip(expected_keys, expected_types):
        if key not in in_data:
            return "Key {} is missing from input".format(key)
        if type(in_data[key]) is not value_type:
            return "Key {} has the incorrect value type".format(key)
    return True


@app.route("/add_test", methods=["POST"])
def post_add_test():
    """POST route to receive information about a test to add to a patient
    record in the database.

    This "Flask handler" function receives a POST request to add a test result
    to a patient record in the database.  The POST request should receive a
    dictionary encoded as a JSON string in the following format:

        {"id": int,
         "test_name": str,
         "test_result": int}

    The value of "id" is an integer that is the medical record number for the
    patient.  The value of "test_name" is a string containing the name of the
    test.  The value of "test_result" is an integer containing the numeric
    result of the test.

    The function first receives the dictionary sent with the POST request.  It
    then calls a driver function to act on the data.  It finally returns the
    resulting message and status code.
    """

    in_data = request.get_json()
    answer, status_code = add_test_driver(in_data)
    return jsonify(answer), status_code


def does_patient_exist_in_db(patient_id):
    """Determines whether a patient exists in the database based on a given id
    number

    This function accepts a patient id (medical record number) as an input
    parameter.  It then queries the MongoDB database, using the patient id
    as the primary key search parameter.  If the record does not exist, an
    exception will be thrown which is captured in a try/except block, allowing
    the function to return False, indicating that the record does not exist
    in the database.  If the record does exist, the function will return True.

    Args:
        patient_id (int): patient medical record number to search for in the
            database

    Returns:
        bool: True if patient exists in database, False otherwise

    """
    try:
        db_item = Patient.objects.raw({"_id": patient_id}).first()
    except pymodm_errors.DoesNotExist:
        return False
    return True


def add_test_driver(in_data):
    """Implements the '/add_test' route

    This function performs the data validation and implementation for the
    `/add_test` route which adds a new test result to the database entry
    for a specific patient.  It first calls a function that validates that
    the necessary keys and value data types exist in the input dictionary.
    If the necessary information does not exist, the function returns an
    error message and a status code of 400.  Next, another function is called
    to verify the specified patient exists in the database.  If not, an error
    message and a status code of 400 is returned.  Otherwise, another function
    is called and sent the necessary information to add the test results to
    the correct patient.  A success message and a 200 status code is then
    returned.

    Args:
        in_data (dict): Data received from the POST request.  Should be a
        dictionary with the format found in the docstring of the
        "post_add_test" function, but that needs to be verified

    Returns:
        str, int: a message with information about the success or failure of
            the operation and a status code
        """

    expected_keys = ["id", "test_name", "test_result"]
    expected_types = [int, str, int]
    validation = validate_input_data_generic(in_data, expected_keys,
                                             expected_types)
    if validation is not True:
        return validation, 400
    does_id_exist = does_patient_exist_in_db(in_data["id"])
    if does_id_exist is False:
        return "Patient id {} does not exist in database"\
            .format(in_data["id"]), 400
    add_test_to_db(in_data["id"], in_data["test_name"],
                   in_data["test_result"])
    return "Test successfully added", 200


@app.route("/get_results/<patient_id>", methods=["GET"])
def get_get_results(patient_id):
    """GET route to obtain results for a specific patient

    This function implements a variable URL in which the server returns
    patient information.  The variable URL will contain the medical record
    number, or id, of the patient of interest.  This id is passed to a function
    that will retrieve the data for this function to return.

    Args:
        patient_id (str): the variable portion of the URL which should contain
            the patient medical record number

    Returns:
        str, int: message on result of request and the status code

    """
    answer, status = get_results_driver(patient_id)
    return jsonify(answer), status


def get_results_driver(patient_id):
    """Implements the "/get_results/<patient_id>" route

    This function receives, as a string, the portion of the variable URL that
    should contain the id number of the patient to retrieve.  The function
    first calls a validation function to ensure that the patient id is valid
    and that the patient exists in the database.  If not, an error message is
    returned with a status code of 400.  If the patient id is valid and there
    is a patient with that id, a call is made to a function to retrieve that
    patient, and the patient dictionary is returned with a status code of 200.

    Args:
        patient_id (str): patient id found in variable URL

    Returns:
        str, int: error message and 400 status code if patient_id parameter is
                    invalid, or
        list, int: list of test results and 200 status code if patient_id
                    matches an entry in database

    """
    validation = validate_patient_id_from_get(patient_id)
    if validation is not True:
        return validation, 400
    test_list = get_patient_test_results_from_database(int(patient_id))
    return test_list, 200


def get_patient_test_results_from_database(patient_id):
    """Retrieves a patient test results from the database based on the given
       id.

    This function takes the patient_id sent as a parameter and queries the
    MongoDB database using this id to find the patient of interest.  The
    patient_id has already been verified to be in the database, so the query
    is not done in a try/except block.  Once the record is retrieved, the
    "tests" list is returned.

    Note: if the database is not yet available for use, this function could be
    "mocked" to provide a made-up response.

    Args:
        patient_id (int): the patient id of interest

    Returns:
        list: patient test results
    """
    db_item = Patient.objects.raw({"_id": patient_id}).first()
    return db_item.tests


def validate_patient_id_from_get(patient_id):
    """Validates that received patient id is an integer and that patient exists

    This function validates the information received by the variable URL
    "/get_results/<patient_id>".  First, it checks that the "patient_id"
    received represents a number.  It then checks that a patient exists in the
    database with that number.  If either of these conditions is not true,
    an error message string is returned.  If both are true, a value of True
    is returned to indicate a valid input.

    Args:
        patient_id (str): The portion of the variable URL that should
            contain the patient ID

    Returns:
        str: error message if validation fails, or
        bool: True if validation passes

    """
    try:
        patient_num = int(patient_id)
    except ValueError:
        return "Patient_id should be an integer"
    if does_patient_exist_in_db(patient_num) is False:
        return "Patient_id of {} does not exist in database"\
            .format(patient_num)
    return True


if __name__ == '__main__':
    init_server()
    app.run()
