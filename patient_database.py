db = {}

class Patient:
    """
    Represents a patient in the system.

    Attributes:
        mrn (str): Medical Record Number, used as a unique identifier.
        email (str): Patient's email address.
        age (int): Patient's age.
        tests (list): List of test records associated with the patient.
    """

    def __init__(self, mrn, email, age, tr):
        """
        Initialize a new Patient instance.

        Args:
            mrn (str): Medical Record Number.
            email (str): Patient's email address.
            age (int): Patient's age.
            tr (list): Initial list of test records.
        """
        self.mrn = mrn
        self.email = email
        self.age = age
        self.tests = tr


def create_patient(mrn, email, age):
    """
    Create a new patient and store it in the in-memory database.

    Args:
        mrn (str): Medical Record Number (unique identifier).
        email (str): Patient's email address.
        age (int): Patient's age.

    Returns:
        Patient: The newly created Patient object.

    Notes:
        If a patient with the same MRN already exists, it will be overwritten.
    """
    patient = Patient(mrn, email, age, [])
    db[mrn] = patient
    return patient


def get_patient(mrn):
    """
    Retrieve a patient from the database by MRN.

    Args:
        mrn (str): Medical Record Number.

    Returns:
        Patient | None: The Patient object if found, otherwise None.
    """
    return db.get(mrn)