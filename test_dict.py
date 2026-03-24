import patient_database
import datetime

test_dict = {}


class Test:
    def __init__(self, name, timestamp, mrn,
                 phys_email, mylab_email, status, age):
        self.name = name
        self.timestamp = timestamp
        self.mrn = mrn
        self.phys_email = phys_email
        self.labemail = mylab_email
        self.test_r = None
        self.status = status
        self.age = age


def create_test(mrn, name):
    from lab_server import lab_email
    patient = patient_database.get_patient(mrn)
    phys_email = patient.email
    mylab_email = lab_email
    age = patient.age
    now = datetime.datetime.now()
    timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
    status = 'pending'
    test = Test(name, timestamp, mrn, phys_email, mylab_email, status, age)
    test_dict[(mrn, name)] = test
    # NOTE: need to send email here
    return test


def get_test(mrn, name):
    return test_dict.get((mrn, name))
