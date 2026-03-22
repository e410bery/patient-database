db = {}


class Patient:
    def __init__(self, mrn, email, age, tr):
        self.mrn = mrn
        self.email = email
        self.age = age
        self.tests = tr


def create_patient(mrn, email, age):
    patient = Patient(mrn, email, age, [])
    db[mrn] = patient
    return patient


def get_patient(mrn):
    return db.get(mrn)


def get_patient_phys_email(mrn):
    patient = get_patient(mrn)
    return patient.email
