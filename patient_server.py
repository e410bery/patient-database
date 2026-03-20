import lab_server

db = {}

class Patient:
    def __init__(self, mrn, email, age, tr):
        self.mrn = mrn
        self.email = email
        self.age = age
        self.tests = tr