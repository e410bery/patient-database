test_dict = {}


class Test:
    def __init__(self, name, timestamp, mrn,
                 phys_email, lab_email, test_r, status):
        self.name = name
        self.timestamp = timestamp
        self.mrn = mrn
        self.phys_email = phys_email
        self.lab_email = lab_email
        self.test_r = test_r
        self.status = status
