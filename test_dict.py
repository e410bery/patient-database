import patient_database
import datetime

test_dict = {}


class Test:
    def __init__(self, name, timestamp, mrn,
                 phys_email, mylab_email, status, age):
        self.name = name
        self.timestamp = [timestamp]
        self.test_r = []
        self.mrn = mrn
        self.phys_email = phys_email
        self.lab_email = mylab_email
        self.status = [status]
        self.age = age

    def append_request(self):
        import lab_server
        now = datetime.datetime.now()
        timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
        subject = f"New test request: MRN {self.mrn}, Test {self.name}"
        content = (f"Patient MRN: {self.mrn}, Test: {self.name}, "
                   f"Requested: {timestamp}")
        lab_server.send_email(self.phys_email, self.lab_email, subject,
                              content)
        self.status.append("pending")
        self.timestamp.append(timestamp)


def create_test(mrn, name):
    from lab_server import lab_email
    import lab_server
    patient = patient_database.get_patient(mrn)
    phys_email = patient.email
    mylab_email = lab_email
    age = patient.age
    now = datetime.datetime.now()
    timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
    status = 'pending'
    test = Test(name, timestamp, mrn, phys_email, mylab_email, status, age)
    test_dict[(mrn, name)] = test
    subject = f"New test request: MRN {mrn}, Test {name}"
    content = (f"Patient MRN: {mrn}, Test: {name}, "
               f"Requested: {timestamp}")
    lab_server.send_email(phys_email, mylab_email, subject, content)
    return test


def get_test(mrn, name):
    return test_dict.get((mrn, name))
