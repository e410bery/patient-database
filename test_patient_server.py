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
    from patient_database import db
    assert len(db) == 1
    assert db[123].age == 21


def test_new_patient_bad_mrn(client):
    in_json = {"patient_mrn": "1a",
               "attending_email": 'emf55@duke.edu',
               "patient_age": 21}
    response = client.post("/patient/new_patient", json=in_json)
    assert response.status_code == 400
    assert response.data.decode() == "Invalid MRN"


def test_new_patient_bad_age(client):
    in_json = {"patient_mrn": "123",
               "attending_email": 'emf55@duke.edu',
               "patient_age": "nine"}
    response = client.post("/patient/new_patient", json=in_json)
    assert response.status_code == 400
    assert response.data.decode() == "Invalid Age"


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
    response = client.post("/patient/results/interval_average")
    assert response.status_code == 200
    assert response.data.decode() == "Interval Average: "


@pytest.mark.parametrize(
    "input_val, expected",
    [
        (25, 25),
        ("30", 30),
        ("0", 0),
        ("a14", None),
        (3.14, None),
        ("3.14", None),
        ("abc", None),
        ("", None),
        (None, None),
    ])
def test_validate_mrn_age(input_val, expected):
    from patient_server import validate_mrn_age
    assert validate_mrn_age(input_val) == expected
