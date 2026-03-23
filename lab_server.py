from flask import Flask, request, jsonify

lab_email = ""
open_requests = []
lab_tests_available = ["HR", "HDL", "LDL", "TSH"]


def lab_routes(app):

    @app.route('/lab/email_address', methods=['POST'])
    def register_lab_email():
        data = request.get_json()
        # parse and store email
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
