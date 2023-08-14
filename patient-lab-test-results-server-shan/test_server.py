import pytest


def test_add_new_patient():
    from server import add_new_patient
    patient_mrn = "12305"
    attending_email = "shanshan.gao@duke.edu"
    patient_age = 12
    from server import db
    add_new_patient(patient_mrn, attending_email, patient_age)
    assert db[patient_mrn]["patient_mrn"] == patient_mrn


@pytest.mark.parametrize("in_data, expected", [
    ({"patient_mrn": "12305", "attending_email":
        "shanshan.gao@duke.edu", "patient_age": "12"}, True),
    ({"patient_mrn": "12305", "attendingemail":
        "shanshan.gao@duke.edu", "patient_age": "12"},
     "key attending_email is missing from input"),
    ({"patient_mrn": "12305", "attending_email":
        "shanshan.gao@duke.edu"}, "key patient_age is missing from input"),
    (["One", 123, "O+"], "Input is not dictionary"),
])
def test_validate_input_data_keys_new_patient(in_data, expected):
    from server import validate_input_data_keys_new_patient
    answer = validate_input_data_keys_new_patient(in_data)
    assert answer == expected


@pytest.mark.parametrize("in_data, expected", [
    ({"patient_mrn": 12305, "attending_email":
        "shanshan.gao@duke.edu", "patient_age": "12"}, True),
    ({"patient_mrn": "12305", "attending_email":
        "shanshan.gao@duke.edu", "patient_age": 12}, True),
    ({"patient_mrn": "One", "attending_email":
        "shanshan.gao@duke.edu", "patient_age": "12"},
     "Patient_mrn should be an integer"),
    ({"patient_mrn": "12305", "attending_email": 13, "patient_age": "12"},
     "attending_email should be a a string"),
    ({"patient_mrn": 12305, "attending_email":
        "shanshan.gao@duke.edu", "patient_age": "abc"},
     "patient_age should be an integer")
])
def test_validate_in_data_type(in_data, expected):
    from server import validate_in_data_type
    answer = validate_in_data_type(in_data)
    assert answer == expected


@pytest.mark.parametrize("in_data, expected", [
    ({"patient_mrn": "12305", "attending_email":
        "shanshan.gao@duke.edu", "patient_age": "12"}, 200),
    ({"patient_mrn": "abc", "attending_email":
        "shanshan.gao@duke.edu", "patient_age": "12"}, 400),
    ({"patient_mrn": "12305", "attending_email":
        123, "patient_age": "12"}, 400),
    ({"patient_mrn": "12305", "attending_email":
        "shanshan.gao@duke.edu", "patient_age": "abc"}, 400),
    ({"patient_mrn": "12305",
      "attending_email": "shanshan.gao@duke.edu"}, 400),
])
def test_new_patient_driver(in_data, expected):
    from server import new_patient_driver
    answer = new_patient_driver(in_data)
    if expected == 200:
        from server import db, add_new_patient
        add_new_patient(in_data["patient_mrn"],
                        in_data["attending_email"], in_data["patient_age"])
        assert db[in_data["patient_mrn"]]["patient_mrn"]\
               == in_data["patient_mrn"]
    assert answer[1] == expected
