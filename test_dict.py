import patient_database
import datetime

test_dict = {}


class Test:
    """
    Represents a medical test request for a patient.

    Attributes:
        name (str): Name of the test.
        timestamp (list[str]): List of timestamps when requests were made.
        test_r (list): Placeholder for test results.
        mrn (str): Medical Record Number identifying the patient.
        phys_email (str): Email address of the requesting physician.
        lab_email (str): Email address of the lab receiving the request.
        status (list[str]): Status history of the test (e.g., pending, completed).
        age (int): Patient's age.
    """

    def __init__(self, name, timestamp, mrn,
                 phys_email, mylab_email, status, age):
        """
        Initialize a Test instance.

        Args:
            name (str): Name of the test.
            timestamp (str): Initial timestamp of the request.
            mrn (str): Patient's Medical Record Number.
            phys_email (str): Physician's email address.
            mylab_email (str): Lab email address.
            status (str): Initial status of the test.
            age (int): Patient's age.
        """
        self.name = name
        self.timestamp = [timestamp]
        self.test_r = []
        self.mrn = mrn
        self.phys_email = phys_email
        self.lab_email = mylab_email
        self.status = [status]
        self.age = age

    def append_request(self):
        """
        Append a new test request for this patient.

        Sends an email notification to the lab and updates the test's
        status and timestamp history.
        """
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
    """
    Create a new test request for a patient.

    Retrieves patient information, initializes a Test object,
    stores it in the global test dictionary, and sends a notification
    email to the lab.

    Args:
        mrn (str): Patient's Medical Record Number.
        name (str): Name of the test.

    Returns:
        Test: The created Test object.
    """
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
    """
    Retrieve a test by patient MRN and test name.

    Args:
        mrn (str): Patient's Medical Record Number.
        name (str): Name of the test.

    Returns:
        Test | None: The corresponding Test object if found, otherwise None.
    """
    return test_dict.get((mrn, name))