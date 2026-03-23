import lab_server
import patient_database
from flask import Flask, request


def validate_mrn_age(val):
    if type(val) is int:
        return val
    if type(val) is float:
        return None
    try:
        return int(val)
    except:
        return None


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
        patient_database.create_patient(mrn,
                                       email,
                                       age)
        return "Added Patient", 200

    @app.route('/patient/new_request', methods=['POST'])
    def new_request():

        return "Added Request", 200

    @app.route('/patient/results/<patient_mrn>', methods=['GET'])
    def get_patient(patient_mrn):
        # to be implemented by nika
        return f"Got patient {patient_mrn}", 200

    @app.route('/patient/results/<patient_mrn>/<test_name>', methods=['GET'])
    def get_available_results(patient_mrn, test_name):
        return f"Available results for patient {patient_mrn}: {test_name}", 200

    @app.route('/patient/results/<patient_mrn>/<test_name>/average',
               methods=['GET'])
    def get_average_result(patient_mrn, test_name):
        return "Average result: ", 200

    @app.route('/patient/results/interval_average', methods=['POST'])
    def get_interval_average():
        return "Interval Average: ", 200


def main():
    return


if __name__ == "__main__":
    main()
