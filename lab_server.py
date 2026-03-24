from flask import Flask, request, jsonify

app = Flask(__name__)
lab_email = ""
open_requests = []
lab_tests_available = ["HR", "HDL", "LDL", "TSH"]


def validate_mrn(mrn):
    try:
        result = int(mrn)
        return result if result > 0 else False
    except ValueError:
        return False


def is_abnormal(test_name, test_result, age):
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


def lab_routes(app):

    @app.route('/lab/email_address', methods=['POST'])
    def register_lab_email():
        data = request.get_json()
        return "Lab email registered", 200

    @app.route('/lab/list_available_tests', methods=['GET'])
    def list_available_tests():
        return jsonify(lab_tests_available), 200

    @app.route('/lab/open_requests', methods=['GET'])
    def post_open_requests():
        return jsonify(open_requests)

    @app.route('/lab/new_result', methods=['POST'])
    def post_new_result():
        return "Result received", 200
