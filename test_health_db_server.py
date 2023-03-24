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

