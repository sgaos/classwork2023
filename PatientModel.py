from pymodm import MongoModel, fields


class Patient(MongoModel):
    patient_id = fields.IntegerField(primary_key=True)
    patient_name = fields.CharField()
    blood_type = fields.CharField()
    tests = fields.ListField()
