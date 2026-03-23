import pytest
from server import app
from lab_server import lab_routes

lab_routes(app)


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
