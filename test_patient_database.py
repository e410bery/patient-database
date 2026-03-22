import pytest


def test_init():
    from patient_database import Patient
    new_instance = Patient(123, "emf55@duke.edu", 21, [])
    answer = new_instance.mrn
    expected_mrn = 123
    assert answer == expected_mrn


def test_create_patient():
    from patient_database import create_patient, db
    db.clear()
    created = create_patient(123, 'emf55@duke.edu', 21)
    expected_mrn = 123
    assert len(db) == 1
    assert db[123] == created


def test_get_patient():
    from patient_database import db, Patient, get_patient
    db.clear()
    db[123] = Patient(123, "emf", 21, [])
    found = get_patient(123)
    assert found.age == 21


def test_get_patient_none():
    from patient_database import db, get_patient
    db.clear()
    assert get_patient(123) is None


def test_get_patient_phys_email():
    from patient_database import db, create_patient, get_patient_phys_email
    db.clear()
    email = "test_email"
    created = create_patient(123, email, 21)
    assert get_patient_phys_email(123) == email
