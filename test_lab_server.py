import pytest
import lab_server
from server import app
from patient_database import db, Patient
from lab_server import lab_routes, validate_mrn, is_abnormal
import test_dict

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


def test_register_lab_email_success(client):
    response = client.post('/lab/email_address',
                           json={"email": "lab@hospital.com"})
    assert response.status_code == 200


def test_register_lab_email_missing_key(client):
    response = client.post('/lab/email_address',
                           json={"wrong_key": "lab@hospital.com"})
    assert response.status_code == 400


def test_register_lab_email_not_string(client):
    response = client.post('/lab/email_address',
                           json={"email": 123})
    assert response.status_code == 400


def test_register_lab_email_empty_body(client):
    response = client.post('/lab/email_address', json={})
    assert response.status_code == 400


def test_list_available_tests(client):
    response = client.get('/lab/list_available_tests')
    assert response.status_code == 200
    assert response.get_json() == ["HR", "HDL", "LDL", "TSH"]


def test_open_requests_empty(client):
    response = client.get('/lab/open_requests')
    assert response.status_code == 200
    assert response.get_json() == []


def test_open_requests_with_data(client):
    lab_server.open_requests.append({
        "patient_mrn": 123,
        "test_name": "HR",
        "request_timestamp": "2018-03-19 11:00:36"
    })
    response = client.get('/lab/open_requests')
    assert response.status_code == 200
    assert len(response.get_json()) == 1
    assert response.get_json()[0]["patient_mrn"] == 123
    assert response.get_json()[0]["test_name"] == "HR"
    lab_server.open_requests.clear()


def test_new_result_invalid_test_name(client):
    db[123] = Patient(123, "doc@hospital.com", 25, [])
    test_dict.create_test(123, "HDL")
    response = client.post('/lab/new_result',
                           json={"patient_mrn": 123,
                                 "test_name": "INVALID",
                                 "test_result": 70})
    assert response.status_code == 400


@pytest.fixture(autouse=True)
def reset_state():
    import test_dict as td
    db.clear()
    td.test_dict.clear()
    lab_server.open_requests.clear()
    yield
    db.clear()
    td.test_dict.clear()
    lab_server.open_requests.clear()


def test_new_result_invalid_test_result_type(client):
    db[123] = Patient(123, "doc@hospital.com", 25, [])
    test_dict.create_test(123, "HDL")
    response = client.post('/lab/new_result',
                           json={"patient_mrn": 123,
                                 "test_name": "HDL",
                                 "test_result": "seventy"})
    assert response.status_code == 400


def test_new_result_test_not_found(client):
    db[123] = Patient(123, "doc@hospital.com", 25, [])
    response = client.post('/lab/new_result',
                           json={"patient_mrn": 123,
                                 "test_name": "HDL",
                                 "test_result": 70})
    assert response.status_code == 400


def test_new_result_success(client):
    db[123] = Patient(123, "doc@hospital.com", 25, [])
    test_dict.create_test(123, "HDL")
    response = client.post('/lab/new_result',
                           json={"patient_mrn": 123,
                                 "test_name": "HDL",
                                 "test_result": 70})
    assert response.status_code == 200
    assert response.data.decode() == "Result received"


def test_new_result_stores_result(client):
    db[123] = Patient(123, "doc@hospital.com", 25, [])
    test_dict.create_test(123, "HDL")
    client.post('/lab/new_result',
                json={"patient_mrn": 123,
                      "test_name": "HDL",
                      "test_result": 70})
    assert test_dict.get_test(123, "HDL").test_r == [70]


def test_new_result_missing_json(client):
    response = client.post('/lab/new_result',
                           content_type='application/json')
    assert response.status_code == 400


def test_new_result_missing_key(client):
    response = client.post('/lab/new_result',
                           json={"patient_mrn": 123,
                                 "test_name": "HDL"})
    assert response.status_code == 400


def test_new_result_invalid_mrn(client):
    response = client.post('/lab/new_result',
                           json={"patient_mrn": "abc",
                                 "test_name": "HDL",
                                 "test_result": 70})
    assert response.status_code == 400


def test_new_result_patient_not_found(client):
    response = client.post('/lab/new_result',
                           json={"patient_mrn": 999,
                                 "test_name": "HDL",
                                 "test_result": 70})
    assert response.status_code == 400


def test_new_result_abnormal_sets_status(client):
    db[123] = Patient(123, "doc@hospital.com", 25, [])
    test_dict.create_test(123, "HDL")
    client.post('/lab/new_result',
                json={"patient_mrn": 123,
                      "test_name": "HDL",
                      "test_result": 50})
    assert test_dict.get_test(123, "HDL").status == ["Abnormal"]


def test_new_result_normal_sets_status(client):
    db[123] = Patient(123, "doc@hospital.com", 25, [])
    test_dict.create_test(123, "HDL")
    client.post('/lab/new_result',
                json={"patient_mrn": 123,
                      "test_name": "HDL",
                      "test_result": 70})
    assert test_dict.get_test(123, "HDL").status == ["Normal"]
