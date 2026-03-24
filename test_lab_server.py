import pytest
from server import app
from lab_server import lab_routes, validate_mrn

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


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_register_lab_email(client):
    response = client.post('/lab/email_address',
                           json={"email": "lab@hospital.com"})
    assert response.data.decode() == "Lab email registered"
    assert response.status_code == 200


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
