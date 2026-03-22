import pytest
from server import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_server_status(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.data.decode() == "Server is running"


def test_patient_server_status(client):
    response = client.get("/patient")
    assert response.status_code == 200
    assert response.data.decode() == "Patient Server is running"


def test_new_patient(client):
    in_json = {"patient_mrn": 123,
               "attending_email": 'emf55@duke.edu',
               "patient_age": 21}
    response = client.post("/patient/new_patient", json=in_json)
    assert response.status_code == 200
    assert response.data.decode() == "Added Patient"


def test_new_request(client):
    response = client.post("/patient/new_request")
    assert response.status_code == 200
    assert response.data.decode() == "Added Request"


def test_get_patient(client):
    mrn = "12345"
    response = client.get(f"/patient/results/{mrn}")
    assert response.status_code == 200
    assert response.data.decode() == f"Got patient {mrn}"


def test_get_available_results(client):
    mrn = "12345"
    test_name = "HDL"
    response = client.get(f"/patient/results/{mrn}/{test_name}")
    assert response.status_code == 200
    assert response.data.decode() == f"Available results for " \
                                     f"patient {mrn}: {test_name}"


def test_get_average_result(client):
    mrn = "12345"
    test_name = "HDL"
    response = client.get(f"/patient/results/{mrn}/{test_name}/average")
    assert response.status_code == 200
    assert response.data.decode() == "Average result: "


def test_get_interval_average(client):
    response = client.get("/patient/results/interval_average")
    assert response.status_code == 200
    assert response.data.decode() == "Interval Average: "
