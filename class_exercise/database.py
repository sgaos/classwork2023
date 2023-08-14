def create_patient_entry(First_Name,Last_Name, MRN,
                                 Age):
    new_patient = {}
    new_patient["First Name"] = First_Name
    new_patient["Last Name"] = Last_Name
    new_patient["MRN"] = MRN
    new_patient["Age"] = Age
    new_patient["Tests"] = []
    return new_patient

def get_full_name(new_patient):
    first_name = new_patient["First Name"]
    Last_name = new_patient["Last Name"]
    name = str(first_name) + " " + str(Last_name)
    return name

def print_database(new_patient):
    name = get_full_name(new_patient)
    print("MRN: {}, Full Name: {}, Age: {}".format(new_patient["MRN"], name, new_patient["Age"]))
    return

def get_patient_entry(db, mrn_to_find):
    for patient in db:
        if patient["MRN"] == mrn_to_find:
            return patient
    return False

def add_test_to_patient(db, mrn_to_find, test_name, test_value):
    patient = get_patient_entry(db, mrn_to_find)
    if patient is False:
        print("Bad entry")
    else:
        patient["Tests"] = [test_name, test_value]
    return patient

def get_test_result(db, mrn, test_name):
    patient = get_patient_entry(db, mrn)
    test_value = get_test_value_from_test_list(patient["Tests"], test_name)
    return test_value

def get_test_value_from_test_list(test, test_name):
        if test[0] == test_name:
            return test[1]
        else:
            return "False"

def minor_or_adult(patient):
    age = int(patient["Age"])
    if age >= 18:
        return "Adult"
    else:
        return "minor"

def main_driver():
    db = []
    db.append(create_patient_entry("Ann", "Ables", 1, 34))
    db.append(create_patient_entry("Bob", "Boyles", 2, 45))
    db.append(create_patient_entry("Chris", "Chou", 3, 2))
    print(db)
    for patient in db:
        print_database(patient)
        print("{} is {}".format(get_full_name(patient),minor_or_adult(patient)))
    add_test_to_patient(db, 1, "HDL", 120)
    add_test_to_patient(db, 2, "LDL", 100)
    add_test_to_patient(db, 3, "HDL", 99)
    room_numbers = ["103", "232", "333"]
    print(db)
    print(get_test_result(db, 2, "LDL"))

if __name__ == "__main__":
    main_driver()