import lab_server
from flask import Flask, request


def patient_routes(app):
    @app.route('/patient/new_patient', methods=['POST'])
    def new_patient():
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

    @app.route('/patient/results/interval_average', methods=['GET'])
    def get_interval_average():
        return "Interval Average: ", 200


def main():
    return


if __name__ == "__main__":
    main()
