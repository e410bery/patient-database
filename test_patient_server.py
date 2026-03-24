import pytest
from server import app
import patient_database


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


def test_new_patient_bad_email(client):
    in_json = {"patient_mrn": "123",
               "attending_email": 123,
               "patient_age": "9"}
    response = client.post("/patient/new_patient", json=in_json)
    assert response.status_code == 400
    assert response.data.decode() == "Invalid Email"


def test_new_request_invalid_mrn(client):
    response = client.post(
        "/patient/new_request",
        json={"patient_mrn": "abc", "test_name": "HDL"},
    )
    assert response.status_code == 400
    assert response.data.decode() == "Invalid MRN"


def test_new_request_patient_not_found(client):
    import patient_database
    patient_database.db.clear()
    response = client.post(
        "/patient/new_request",
        json={"patient_mrn": 123, "test_name": "HDL"},
    )
    assert response.status_code == 400
    assert response.data.decode() == "Patient not found"


def test_new_request_test_not_found(client):
    import patient_database
    patient_database.db.clear()
    patient_database.create_patient(123, "emf55", 21)
    response = client.post(
        "/patient/new_request",
        json={"patient_mrn": "123", "test_name": "INVALID_TEST"},
    )
    assert response.status_code == 400
    assert response.data.decode() == "Test not found"


def test_new_request_success(client):
    import patient_database
    patient_database.db.clear()
    patient_database.create_patient(123, "emf55", 21)
    import lab_server
    lab_server.lab_tests_available = ["HDL"]
    response = client.post(
        "/patient/new_request",
        json={"patient_mrn": "123", "test_name": "HDL"},
    )
    assert response.status_code == 200
    assert response.data.decode() == "Added Request"


@pytest.mark.parametrize("mrn", ["abc", "54a"])
def test_invalid_mrn(client, mrn):
    response = client.get(f"/patient/results/{mrn}")
    assert response.status_code == 400


def test_patient_results_no_tests(client):
    patient_database.create_patient(123, "doc@hospital.com", 45)
    data = client.get("/patient/results/1001").get_json()
    assert data["patient_mrn"] == 123
    assert data["completed_tests"] == []
    assert data["open_requests"] == []


def test_one_open_request(client):
    import test_dict
    patient_database.create_patient(124, "doc@hospital.com", 30)

    t = test_dict.Test(
        name="HR",
        timestamp="2024-03-19 11:00:00",
        mrn=124,
        phys_email="doc@hospital.com",
        mylab_email="lab@hospital.com",
        status="pending",
        age=30
    )
    t.test_r = None
    t.result_timestamp = None
    test_dict.test_dict[(124, "HR")] = t

    data = client.get("/patient/results/124").get_json()
    assert data["open_requests"] == [
        {"test_name": "HR", "request_timestamp": "2024-03-19 11:00:00"}
    ]
    assert data["completed_tests"] == []


def test_patient_results_patient_not_in_database(client):
    response = client.get("/patient/results/111")
    assert response.status_code == 400


@pytest.fixture(autouse=True)
def clear_dbs():
    import test_dict
    patient_database.db.clear()
    test_dict.test_dict.clear()
    yield
    patient_database.db.clear()
    test_dict.test_dict.clear()


def test_patient_results_no_tests(client):
    patient_database.create_patient(123, "doc@hospital.com", 45)
    data = client.get("/patient/results/123").get_json()
    response = client.get("/patient/results/123")
    assert response.status_code == 200
    assert data["patient_mrn"] == 123
    assert data["completed_tests"] == []
    assert data["open_requests"] == []


def test_pending_status_goes_to_open_requests(client):
    import test_dict
    patient_database.create_patient(1002, "doc@hospital.com", 30)
    t = test_dict.Test(
        name="HR",
        timestamp="2024-03-19 11:00:00",
        mrn=1002,
        phys_email="doc@hospital.com",
        mylab_email="lab@hospital.com",
        status="pending",
        age=30
    )
    t.test_r = None
    t.result_timestamp = None
    test_dict.test_dict[(1002, "HR")] = t

    data = client.get("/patient/results/1002").get_json()
    assert len(data["open_requests"]) == 1
    assert len(data["completed_tests"]) == 0


def test_non_pending_status_goes_to_completed(client):
    import test_dict
    patient_database.create_patient(1002, "doc@hospital.com", 30)
    t = test_dict.Test(
        name="HR",
        timestamp="2024-03-19 11:00:00",
        mrn=1002,
        phys_email="doc@hospital.com",
        mylab_email="lab@hospital.com",
        status="normal",
        age=30
    )
    t.test_r = 72
    t.result_timestamp = "2024-03-19 12:00:00"
    test_dict.test_dict[(1002, "HR")] = t

    data = client.get("/patient/results/1002").get_json()
    assert len(data["completed_tests"]) == 1
    assert len(data["open_requests"]) == 0


def test_patient_results_format(client):
    patient_database.create_patient(1002, "doc@hospital.com", 30)
    data = client.get("/patient/results/1002").get_json()
    assert "patient_mrn" in data
    assert "completed_tests" in data
    assert "open_requests" in data
    assert data["patient_mrn"] == 1002
    assert isinstance(data["completed_tests"], list)
    assert isinstance(data["open_requests"], list)


def test_get_available_results(client):
    mrn = "12345"
    test_name = "HDL"
    response = client.get(f"/patient/results/{mrn}/{test_name}")
    assert response.status_code == 200
    assert response.data.decode() == f"Available results for " \
                                     f"patient {mrn}: {test_name}"


def test_completed_test_status_abnormal(client):
    import test_dict
    patient_database.create_patient(1003, "doc@hospital.com", 30)
    t = test_dict.Test(
        name="HR",
        timestamp="2024-03-19 11:00:00",
        mrn=1003,
        phys_email="doc@hospital.com",
        mylab_email="lab@hospital.com",
        status="Abnormal",
        age=30
    )
    t.test_r = 120
    t.result_timestamp = "2024-03-19 12:00:00"
    test_dict.test_dict[(1003, "HR")] = t

    data = client.get("/patient/results/1003").get_json()
    assert data["completed_tests"][0]["test_status"] == "Abnormal"
    assert data["completed_tests"][0]["test_result"] == 120


def test_completed_test_status_normal(client):
    import test_dict
    patient_database.create_patient(1004, "doc@hospital.com", 30)
    t = test_dict.Test(
        name="HR",
        timestamp="2024-03-19 11:00:00",
        mrn=1004,
        phys_email="doc@hospital.com",
        mylab_email="lab@hospital.com",
        status="Normal",
        age=30
    )
    t.test_r = 72
    t.result_timestamp = "2024-03-19 12:00:00"
    test_dict.test_dict[(1004, "HR")] = t

    data = client.get("/patient/results/1004").get_json()
    assert data["completed_tests"][0]["test_status"] == "Normal"
    assert data["completed_tests"][0]["test_result"] == 72


def test_determine_test_status_abnormal():
    from patient_server import determine_test_status
    assert determine_test_status("Abnormal") == "Abnormal"


def test_determine_test_status_normal():
    from patient_server import determine_test_status
    assert determine_test_status("Normal") == "Normal"


@pytest.mark.parametrize(
    "inputs, expected",
    [
        ([1, 2, 3], 2.0),
        ([10, 20, 30, 40], 25.0),
        ([5], 5.0),
        ([0, 0, 0], 0.0),
        ([-1, -2, -3], -2.0),
    ],
)
def test_find_average(inputs, expected):
    from patient_server import find_average
    assert find_average(inputs) == expected


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


@pytest.mark.parametrize(
    "dates, start_time, expected",
    [
        (["2025-03-24 10:00:00", "2025-03-24 11:00:00",
          "2025-03-24 12:00:00"], "2025-03-24 11:00:00", 1),
        (["2025-03-24 10:00:00", "2025-03-24 11:00:00",
          "2025-03-24 12:00:00"], "2025-03-24 11:30:00", 2),
        (["2025-01-24 11:00:00", "2025-03-15 11:00:00",
          "2025-04-24 11:00:00"], "2025-03-02 11:00:00", 1),
        (["2025-03-24 10:00:00", "2025-03-24 11:00:00"],
         "2025-03-24 09:00:00", 0),
        (["2025-03-24 10:00:00", "2025-03-24 11:00:00"],
         "2025-03-24 12:00:00", None),
        ([], "2025-03-24 10:00:00", None),
        (["2025-03-24 10:00:00"], "2025-03-24 09:00:00", 0),
    ],
)
def test_find_time_index(dates, start_time, expected):
    from patient_server import find_time_index
    assert find_time_index(dates, start_time) == expected
