from pymodm import connect
from PatientModel import Patient

connect("mongodb+srv://daw_spring:daw_spring@bme547.ba348.mongodb.net/"
        "health_db_2023?retryWrites=true&w=majority")

def test_add_patient_to_db():
    from health_db_server import add_patient_to_db
    patient_id = 234
    patient_name = "Test"
    blood_type = "O+"
    answer = add_patient_to_db(patient_id, patient_name, blood_type)
    x = Patient.objects.raw({"_id": patient_id}).first()
    x.delete()
    assert answer.patient_id == patient_id


def test_add_test_to_db():
    from health_db_server import add_test_to_db
    # Arrange
    patient_id = 123
    patient_name = "Test"
    patient_blood_type = "O+"
    from health_db_server import add_patient_to_db
    add_patient_to_db(patient_id, patient_name, patient_blood_type)
    test_name = "HDL"
    test_value = 150

    # Act
    add_test_to_db(patient_id, test_name, test_value)

    # Assert
    from health_db_server import db
    answer = db[patient_id]["tests"][-1]
    expected = (test_name, test_value)
    db.clear()
    assert answer == expected

