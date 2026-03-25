import lab_server
import patient_database
import test_dict
from datetime import datetime
from flask import Flask, request, jsonify


def validate_mrn_age(val):
    """
    Validate and convert a value into an integer MRN or age.

    Accepts integers directly, attempts to cast strings to integers,
    and rejects floats or invalid types.

    Args:
        val (Any): Input value representing MRN or age.

    Returns:
        int or None: Integer value if valid, otherwise None.
    """
    if type(val) is int:
        return val
    if type(val) is float:
        return None
    try:
        return int(val)
    except TypeError:
        return None
    except ValueError:
        return None


def find_average(results):
    """
    Compute the average of a list of numeric results.

    Args:
        results (list[float | int]): List of numeric values.

    Returns:
        float: The arithmetic mean of the input values.

    Raises:
        ZeroDivisionError: If the input list is empty.
    """
    return sum(results) / len(results)


def find_time_index(dates, start_time_str):
    """
    Find the index of the first timestamp on or after a given start time.

    Args:
        dates (list[str]): List of timestamps as strings in
            "%Y-%m-%d %H:%M:%S" format.
        start_time_str (str): Start time string in the same format.

    Returns:
        int or None: Index of the first matching timestamp, or None if none found.
    """
    start_time = datetime.strptime(start_time_str, "%Y-%m-%d %H:%M:%S")
    idx = None
    for i, d in enumerate(dates):
        current = datetime.strptime(d, "%Y-%m-%d %H:%M:%S")
        if current >= start_time:
            idx = i
            break
    return idx


def determine_test_status(status):
    """
    Normalize a test status value.

    Converts any status that is not explicitly "Abnormal" to "Normal".

    Args:
        status (str): Input test status.

    Returns:
        str: "Abnormal" if input is "Abnormal", otherwise "Normal".
    """
    return "Abnormal" if status == "Abnormal" else "Normal"


def get_times(mrn, test):
    """
    Retrieve timestamps for a patient's test, excluding pending entries.

    If the most recent test status is "pending", its timestamp is excluded.

    Args:
        mrn (int): Patient medical record number.
        test (str): Name of the test.

    Returns:
        list[str]: List of timestamp strings.
    """
    test = test_dict.get_test(mrn, test)
    if test.status[-1] == "pending":
        return test.timestamp[0:len(test.timestamp)-1]
    return test.timestamp


def patient_routes(app):
    """
    Register all patient-related API routes on a Flask app.

    This function defines endpoints for:
    - Server status check
    - Creating new patients
    - Submitting test requests
    - Retrieving test results
    - Computing averages (overall and interval-based)

    Args:
        app (Flask): Flask application instance.

    Returns:
        None
    """

    @app.route('/patient', methods=['GET'])
    def patient_server_status():
        """
        Check if the patient server is running.

        Returns:
            str: Status message.
        """
        return "Patient Server is running"

    @app.route('/patient/new_patient', methods=['POST'])
    def new_patient():
        """
        Create a new patient record.

        Expects JSON payload with:
            - patient_mrn (int or str)
            - patient_age (int or str)
            - attending_email (str)

        Returns:
            tuple: (message, status_code)
        """
        mrn = request.json["patient_mrn"]
        mrn = validate_mrn_age(mrn)
        if mrn is None:
            return "Invalid MRN", 400
        age = request.json["patient_age"]
        age = validate_mrn_age(age)
        if age is None:
            return "Invalid Age", 400
        email = request.json["attending_email"]
        if type(email) is not str:
            return "Invalid Email", 400
        patient_database.create_patient(mrn, email, age)
        return "Added Patient", 200

    @app.route('/patient/new_request', methods=['POST'])
    def new_request():
        """
        Create or append a lab test request for a patient.

        Expects JSON payload with:
            - patient_mrn (int or str)
            - test_name (str)

        Returns:
            tuple: (message, status_code)
        """
        mrn = request.json["patient_mrn"]
        mrn = validate_mrn_age(mrn)
        if mrn is None:
            return "Invalid MRN", 400
        patient = patient_database.get_patient(mrn)
        if patient is None:
            return "Patient not found", 400
        test = request.json["test_name"]
        if test not in lab_server.lab_tests_available:
            return "Test not found", 400
        new_test = test_dict.get_test(mrn, test)
        if new_test is None:
            test_dict.create_test(mrn, test)
            return "Added New Request", 200
        else:
            new_test.append_request()
            return "Added Request", 200

    @app.route('/patient/results/<patient_mrn>', methods=['GET'])
    def get_patient_results(patient_mrn):
        """
        Retrieve all test results for a patient.

        Separates completed tests and open (pending) requests.

        Args:
            patient_mrn (str): Patient MRN from URL.

        Returns:
            Response: JSON containing completed tests and open requests.
        """
        mrn = validate_mrn_age(patient_mrn)
        if mrn is None:
            return "Invalid MRN", 400

        patient = patient_database.get_patient(mrn)
        if patient is None:
            return "Patient not found", 400

        completed = []
        open_requests = []

        for (stored_mrn, test_name), test in test_dict.test_dict.items():
            if stored_mrn != mrn:
                continue
            if test.status[-1] == "pending":
                open_requests.append({
                    "test_name": test.name,
                    "request_timestamp": test.timestamp[-1]
                })
                if len(test.status) > 1:
                    for i in range(0, len(test.status)-1):
                        completed.append({
                            "test_name": test.name,
                            "test_result": test.test_r[i],
                            "test_status": test.status[i],
                            "test_timestamp": test.timestamp[i]
                        })
            else:
                for i in range(0, len(test.status)):
                    completed.append({
                        "test_name": test.name,
                        "test_result": test.test_r[i],
                        "test_status": test.status[i],
                        "test_timestamp": test.timestamp[i]
                    })
        return jsonify({
            "patient_mrn": mrn,
            "completed_tests": completed,
            "open_requests": open_requests
        }), 200

    @app.route('/patient/results/<patient_mrn>/<test_name>', methods=['GET'])
    def get_available_results(patient_mrn, test_name):
        """
        Retrieve all recorded results for a specific test.

        Args:
            patient_mrn (str): Patient MRN from URL.
            test_name (str): Name of the test.

        Returns:
            tuple: (list of results, status_code)
        """
        mrn = patient_mrn
        mrn = validate_mrn_age(mrn)
        if mrn is None:
            return "Invalid MRN", 400
        patient = patient_database.get_patient(mrn)
        if patient is None:
            return "Patient not found", 400
        test = test_name
        if test not in lab_server.lab_tests_available:
            return "Test not found", 400
        results = test_dict.get_test(mrn, test).test_r
        return results, 200

    @app.route('/patient/results/<patient_mrn>/<test_name>/average',
               methods=['GET'])
    def get_average_result(patient_mrn, test_name):
        """
        Compute the average result for a specific test.

        Args:
            patient_mrn (str): Patient MRN from URL.
            test_name (str): Name of the test.

        Returns:
            Response: JSON containing the average value.
        """
        mrn = patient_mrn
        mrn = validate_mrn_age(mrn)
        if mrn is None:
            return "Invalid MRN", 400
        patient = patient_database.get_patient(mrn)
        if patient is None:
            return "Patient not found", 401
        test = test_dict.test_dict.get((mrn, test_name))
        if test is None:
            return "Test not found", 402
        results = test.test_r
        return jsonify(find_average(results)), 200

    @app.route('/patient/results/interval_average', methods=['POST'])
    def get_interval_average():
        """
        Compute the average of test results after a specified timestamp.

        Expects JSON payload with:
            - patient_mrn (int or str)
            - test_name (str)
            - average_since (str): Timestamp in "%Y-%m-%d %H:%M:%S" format

        Returns:
            Response: JSON containing the average value.
        """
        mrn = request.json["patient_mrn"]
        test_name = request.json["test_name"]
        start_time = request.json["average_since"]

        mrn = validate_mrn_age(mrn)
        if mrn is None:
            return "Invalid MRN", 400

        patient = patient_database.get_patient(mrn)
        if patient is None:
            return "Patient not found", 400

        if test_name not in lab_server.lab_tests_available:
            return "Test not found", 400

        test = test_dict.test_dict.get((mrn, test_name))
        if test is None:
            return "Test not found", 400

        all_times = get_times(mrn, test_name)
        idx = find_time_index(all_times, start_time)

        if idx is None:
            return f"No results found on/after {start_time}", 400

        interval_results = test.test_r[idx:]

        if not interval_results:
            return f"No results found on/after {start_time}", 400

        avg = find_average(interval_results)
        return jsonify(avg), 200


def main():
    """
    Entry point for the application.

    Currently does nothing.

    Returns:
        None
    """
    return


if __name__ == "__main__":
    main()
