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
