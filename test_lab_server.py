import pytest
import lab_server
from server import app
from lab_server import lab_routes, validate_mrn, is_abnormal

lab_routes(app)


@pytest.mark.parametrize("mrn, expected", [
    (123, 123),
    ("123", 123),
    ("aj", False),
    ("a54", False),
    ("54a", False),
    ("", False),
    (" ", False),
    ("12 3", False),
    ("-123", False),
])
def test_validate_mrn(mrn, expected):
    assert validate_mrn(mrn) == expected


@pytest.mark.parametrize("test_name, test_result, age, expected", [
    ("HDL", 59, 25, True),
    ("HDL", 60, 25, False),
    ("HDL", 70, 25, False),
    ("LDL", 130, 25, True),
    ("LDL", 131, 25, True),
    ("LDL", 129, 25, False),
    ("TSH", 0.9, 25, True),
    ("TSH", 1.0, 25, False),
    ("TSH", 4.0, 25, False),
    ("TSH", 4.1, 25, True),
    ("HR", 152, 1, True),
    ("HR", 151, 1, False),
    ("HR", 138, 3, True),
    ("HR", 137, 3, False),
    ("HR", 134, 5, True),
    ("HR", 133, 5, False),
    ("HR", 131, 8, True),
    ("HR", 130, 8, False),
    ("HR", 120, 12, True),
    ("HR", 119, 12, False),
    ("HR", 101, 16, True),
    ("HR", 100, 16, False),
])
def test_is_abnormal(test_name, test_result, age, expected):
    assert is_abnormal(test_name, test_result, age) == expected


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_register_lab_email_stores_email(client):
    client.post('/lab/email_address',
                json={"email": "lab@hospital.com"})
    assert lab_server.lab_email == "lab@hospital.com"


def test_available_tests(client):
    response = client.get('/lab/list_available_tests')
    assert response.status_code == 200
    assert response.get_json() == ["HR", "HDL", "LDL", "TSH"]


def test_open_requests(client):
    response = client.get('/lab/open_requests')
    assert response.status_code == 200
    assert response.get_json() == []


def test_new_result(client):
    in_json = {"patient_mrn": 123,
               "test_name": "HR",
               "test_result": 80}
    response = client.post('/lab/new_result', json=in_json)
    assert response.status_code == 200
    assert response.data.decode() == "Result received"
