import logging
from flask import Flask
from patient_server import patient_routes
# from lab_server import lab_routes

# Configure logging
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
)

app = Flask(__name__)

# connect routes
patient_routes(app)
# lab_routes(app)

@app.route('/', methods=['GET'])
def server_status():
    return "Server is running"

if __name__ == "__main__":
    app.run()