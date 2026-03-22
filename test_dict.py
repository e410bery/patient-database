import lab_server
from patient_database import get_patient_phys_email
import datetime

test_dict = {}


class Test:
    def __init__(self, name, timestamp, mrn,
                 phys_email, lab_email, status):
        self.name = name
        self.timestamp = timestamp
        self.mrn = mrn
        self.phys_email = phys_email
        self.lab_email = lab_email
        self.test_r = None
        self.status = status


def create_test(mrn, name):
    phys_email = get_patient_phys_email(mrn)
    lab_email = lab_server.lab_email
    now = datetime.datetime.now()
    timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
    status = 'pending'
    test = Test(name, timestamp, mrn, phys_email, lab_email, status)
    test_dict[(mrn, name)] = test
    # NOTE: need to send email here
    return test


def get_test(mrn, name):
    return test_dict.get((mrn, name))
