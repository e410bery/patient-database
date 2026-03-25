from flask import Flask, request, jsonify
import requests
import logging
from datetime import datetime
from test_dict import get_test

lab_email = ""
open_requests = []
lab_tests_available = ["HR", "HDL", "LDL", "TSH"]


def validate_mrn(mrn):
    '''Validates patient mrn to be a positive integer.

    Accepts integers or numeric strings. Rejects strings containing letters.

    Args:
        mrn: the raw MRN value (int or str)

    Returns:
        int: the MRN as an integer, or False if invalid
    '''
    try:
        result = int(mrn)
        return result if result > 0 else False
    except ValueError:
        return False


def is_abnormal(test_name, test_result, age):
    '''Determine whether a test result is abnormal.

    Args:
        test_name (str): one of "HR", "HDL", "LDL", "TSH"
        test_result (int | float): numeric test result
        age (int): patient age in years

    Returns:
        bool: True if the result is abnormal,
        False otherwise
    '''
    if test_name == "HDL":
        return test_result < 60
    if test_name == "LDL":
        return test_result >= 130
    if test_name == "TSH":
        return test_result < 1.0 or test_result > 4.0
    if test_name == "HR":
        if age <= 2:
            return test_result > 151
        elif age <= 4:
            return test_result > 137
        elif age <= 7:
            return test_result > 133
        elif age <= 11:
            return test_result > 130
        elif age <= 15:
            return test_result > 119
        else:
            return test_result > 100
    return False

def send_email(from_email, to_email, subject, content):
    '''Send an e-mail via the simulation server.

    Args:
        from_email (str): sender address
        to_email (str): recipient address
        subject (str): e-mail subject line
        content (str): e-mail body text

    Returns:
        None
    '''
    url = "http://vcm-51187.vm.duke.edu:5007/send_email"
    payload = {"from_email": from_email,
               "to_email": to_email,
               "subject": subject,
               "content": content}
    requests.post(url, json=payload)


def lab_routes(app):
    '''Register all /lab/* routes on the provided Flask app instance.

    Args:
        app: a Flask application instance
    '''
    @app.route('/lab/email_address', methods=['POST'])
    def register_lab_email():
        '''
        Register the lab's e-mail address.

        Accepts JSON: { "email": <email_address> }
        Validates that "email" is present and is a string.

        Returns:
            200 with confirmation message on success.
            400 with error message on validation failure.
        '''
        global lab_email
        data = request.get_json()
        if not data or 'email' not in data:
            return "Missing email", 400
        if type(data['email']) is not str:
            return "Email must be a string", 400
        lab_email = data['email']
        return "Lab email registered", 200

    @app.route('/lab/list_available_tests', methods=['GET'])
    def list_available_tests():
        '''Return a list of all available test names.

        Returns:
        200 with JSON list of available test name strings:
        ["HR", "HDL", "LDL", "TSH"]
        '''
        return jsonify(lab_tests_available), 200

    @app.route('/lab/open_requests', methods=['GET'])
    def get_open_requests():
        '''Return a list of all open test requests.
        Returns:
        200 with JSON list of open request dicts,
        or an empty list if there are no open requests.
        '''
        return jsonify(open_requests), 200

    @app.route('/lab/new_result', methods=['POST'])
    def post_new_result():
        data = request.get_json()
        for key in ["patient_mrn", "test_name", "test_result"]:
            if key not in data:
                return f"Missing key: {key}", 400

        patient_mrn = validate_mrn(data['patient_mrn'])
        if patient_mrn is False:
            return "Invalid MRN", 400
        import patient_database
        patient = patient_database.get_patient(patient_mrn)
        if patient is None:
            return "Patient not found", 400

        if data['test_name'] not in lab_tests_available:
            return "Invalid test name", 400

        if type(data['test_result']) not in [int, float]:
            return "Invalid test result", 400

        test = get_test(patient_mrn, data['test_name'])
        if test is None:
            return "Test request not found", 400

        test_name = data['test_name']
        test_result = data['test_result']
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        test.test_r = test_result
        test.timestamp = timestamp
        abnormal = is_abnormal(test_name, test_result, test.age)
        test.status = "Abnormal" if abnormal else "Normal"

        open_requests[:] = [
            r for r in open_requests
            if not (r["patient_mrn"] == patient_mrn
                    and r["test_name"] == test_name)
        ]

        if abnormal:
            subject = (f"Abnormal result: MRN {patient_mrn}, "
                       f"Test {test_name}")
            content = (f"Patient MRN: {patient_mrn}, Test: {test_name}, "
                       f"Result: {test_result}, Time: {timestamp}")
            send_email(test.lab_email, test.phys_email, subject, content)
            logging.warning(f"Abnormal result: MRN {patient_mrn}, "
                            f"Test {test_name}, Result {test_result}, "
                            f"Attending {test.phys_email}")

        return "Result received", 200
