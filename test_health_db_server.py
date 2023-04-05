import ssl

import pytest
from pymodm import connect
from PatientModel import Patient
from secrets import mongodb_acct, mongodb_pswd

connect("mongodb+srv://{}:{}@bme547.ba348.mongodb.net/"
        "health_db_2023_test_db?retryWrites=true&w=majority"
        .format(mongodb_acct, mongodb_pswd), ssl_cert_reqs=ssl.CERT_NONE)


def test_add_patient_to_db():
    """
    This test shows two ways of checkint that the patient was successfully
    added to the database.

    In "Method 1", the "add_patient_to_db" function returns a copy of what was
    saved to the MongoDB database.  The information in that copy can be
    compared against the known values sent to the database.

    In "Method 2", the MongoDB database is directly queried to ensure that the
    entry exists.

    In both cases, the added entry is deleted from the database.
    """
    from health_db_server import add_patient_to_db
    patient_id = 135
    patient_name = "Ann Ables"
    blood_type = "A+"
    # Method 1
    answer_1 = add_patient_to_db(patient_id, patient_name, blood_type)
    answer_1.delete()
    assert answer_1.patient_name == patient_name
    # Method 2
    # answer_2 = Patient.objects.raw({"_id": patient_id}).first()
    # answer_2.delete()
    # assert answer_2.patient_name == patient_name


def test_add_test_to_db():
    from health_db_server import add_patient_to_db, add_test_to_db
    # Arrange
    patient_id = 123
    patient_name = "Test"
    patient_blood_type = "O+"
    add_patient_to_db(patient_id, patient_name, patient_blood_type)
    test_name = "HDL"
    test_value = 150

    # Act
    add_test_to_db(patient_id, test_name, test_value)

    # Assert
    patient = Patient.objects.raw({"_id": patient_id}).first()
    answer = patient.tests[-1]
    expected = [test_name, test_value]
    patient.delete()
    assert answer == expected


@pytest.mark.parametrize("in_data, expected", [
    ({"name": "One", "id": 123, "blood_type": "A+"}, 200),
    ({"nxme": "One", "id": 234, "blood_type": "O+"}, 400),
    ({"name": "One", "id": 345, "blood_type": 1}, 400)
])
def test_new_patient_driver(in_data, expected):
    """
    This test function focuses mostly on making sure that the algorithmic
    work done in the driver is correct.  More detailed testing of the validate
    function and add_patient_to_db function is done elsewhere.  So, this
    unit test checks for three cases:  a successful addition, a rejection
    based on a missing key, and a rejection based on bad value type.
    """
    from health_db_server import new_patient_driver
    answer = new_patient_driver(in_data)
    if expected == 200:
        patient = Patient.objects.raw({"_id": in_data["id"]}).first()
        expected_name = patient.patient_name
        patient.delete()
        assert expected_name == in_data["name"]
    assert answer[1] == expected


@pytest.mark.parametrize("in_data, expected", [
    ({"name": "One", "id": 123, "blood_type": "A+"}, True),
    ({"nxme": "One", "id": 123, "blood_type": "A+"},
     "Key name is missing from input"),
    ({"name": "One", "id": "abc", "blood_type": "A+"},
     "Key id has the incorrect value type"),
    ({"name": "One", "id": 123, "blood_type": 3},
     "Key blood_type has the incorrect value type"),
    ({"name": 1, "id": 123, "blood_type": "O+"},
     "Key name has the incorrect value type"),
    (["One", 123, "O+"], "Input is not a dictionary"),
])
def test_validate_input_data_generic(in_data, expected):
    from health_db_server import validate_input_data_generic
    expected_keys = ["name", "id", "blood_type"]
    expected_types = [str, int, str]
    answer = validate_input_data_generic(in_data, expected_keys,
                                         expected_types)
    assert answer == expected


@pytest.mark.parametrize("patient_id, expected", [
    (123, True),
    (234, False)
])
def test_does_patient_exist_in_db(patient_id, expected):
    from health_db_server import add_patient_to_db, does_patient_exist_in_db
    # Database starts empty
    patient = add_patient_to_db(123, "TestName", "A+")
    answer = does_patient_exist_in_db(patient_id)
    patient.delete()
    assert answer == expected


@pytest.mark.parametrize("in_data, expected", [
    ({"id": 123, "test_name": "HDL", "test_result": 100}, 200),
    ({"ix": 123, "test_name": "HDL", "test_result": 100}, 400),
    ({"id": 234, "test_name": "LDL", "test_result": 100}, 400),
])
def test_add_test_driver(in_data, expected):
    """
    This test function focuses mostly on making sure that the algorithmic
    work done in the driver is correct.  More detailed testing of the validate
    function and add_patient_to_db function is done elsewhere.  So, this
    unit test checks for three cases:  a successful addition, a rejection
    based on a missing key, and a rejection based on bad value type.
    """
    from health_db_server import add_test_driver, add_patient_to_db
    add_patient_to_db(123, "OneTest", "O+")
    answer = add_test_driver(in_data)
    patient = Patient.objects.raw({"_id": 123}).first()
    if expected == 200:
        answer_test_result = patient.tests[-1][1]
    patient.delete()
    if expected == 200:
        assert answer_test_result == in_data["test_result"]
    assert answer[1] == expected
