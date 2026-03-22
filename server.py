from flask import Flask
from patient_server import patient_routes
# from lab_server import lab_routes

app = Flask(__name__)

# connect patient and lab routes to the main server
patient_routes(app)
# lab_routes(app)


@app.route('/', methods=['GET'])
def server_status():
    return "Server is running"


if __name__ == "__main__":
    app.run()
