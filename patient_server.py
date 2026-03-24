import lab_server
import patient_database
import test_dict
from datetime import datetime
from flask import Flask, request


def validate_mrn_age(val):
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
    return sum(results) / len(results)


def find_time_index(dates, start_time_str):
    start_time = datetime.strptime(start_time_str, "%Y-%m-%d %H:%M:%S")
    idx = None
    for i, d in enumerate(dates):
        current = datetime.strptime(d, "%Y-%m-%d %H:%M:%S")
        if current >= start_time:
            idx = i
            break
    return idx


def patient_routes(app):
    @app.route('/patient', methods=['GET'])
    def patient_server_status():
        return "Patient Server is running"

    @app.route('/patient/new_patient', methods=['POST'])
    def new_patient():
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
        test_dict.create_test(mrn, test)
        return "Added Request", 200

    @app.route('/patient/results/<patient_mrn>', methods=['GET'])
    def get_patient(patient_mrn):
        # to be implemented by nika
        return f"Got patient {patient_mrn}", 200

    @app.route('/patient/results/<patient_mrn>/<test_name>', methods=['GET'])
    def get_available_results(patient_mrn, test_name):
        # mrn = request.json["patient_mrn"]
        # mrn = validate_mrn_age(mrn)
        # if mrn is None:
        #    return "Invalid MRN", 400
        # patient = patient_database.get_patient(mrn)
        # if patient is None:
        #    return "Patient not found", 400
        # test = request.json["test_name"]
        # if test not in lab_server.lab_tests_available:
        #    return "Test not found", 400
        # ask nika how she stored results for completed tests
        # results = test_dict.test_dict[(mrn, test)].results
        # return results, 200
        return f"Available results for patient {patient_mrn}: {test_name}", 200

    @app.route('/patient/results/<patient_mrn>/<test_name>/average',
               methods=['GET'])
    def get_average_result(patient_mrn, test_name):
        results = get_available_results(patient_mrn, test_name)
        # return find_average(results), 200
        return "Average result: ", 200

    @app.route('/patient/results/interval_average', methods=['POST'])
    def get_interval_average():
        # mrn = request.json["patient_mrn"]
        # test_name = request.json["test_name"]
        # start_time = request.json["average_since"]

        # mrn = validate_mrn_age(mrn)
        # if mrn is None:
        #     return "Invalid MRN", 400
        # patient = patient_database.get_patient(mrn)
        # if patient is None:
        #     return "Patient not found", 400
        # test = request.json["test_name"]
        # if test not in lab_server.lab_tests_available:
        #     return "Test not found", 400

        # all_result = get_available_results(mrn, test_name)

        # # find results after start time
        # idx = find_time_index(all_result, start_time)
        # interval_results = all_result[idx:]
        # if interval_results is []:
        #     return f"No results found on/after {start_time}", 400
        # avg = find_average(interval_results)
        # return avg, 200
        return "Interval Average: ", 200


def main():
    return


if __name__ == "__main__":
    main()
