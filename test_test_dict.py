import pytest


def test_init():
    from test_dict import Test
    new_instance = Test(
        "hdl",
        "2026-03-21 10:00:00",
        123,
        "doc@test.com",
        "lab@test.com",
        "pending",
        15,
    )
    assert new_instance.name == "hdl"
    assert new_instance.timestamp == "2026-03-21 10:00:00"
    assert new_instance.mrn == 123
    assert new_instance.phys_email == "doc@test.com"
    assert new_instance.labemail == "lab@test.com"
    assert new_instance.test_r is None
    assert new_instance.status == "pending"
    assert new_instance.age == 15


def test_create_test():
    from patient_database import create_patient
    import lab_server

    lab_server.lab_email = "lab@test.com"
    patient = create_patient(123, "emf55@duke.edu", 21)

    mrn = 123
    name = "hdl"
    result = 55

    from test_dict import test_dict, create_test
    test_dict.clear()

    test = create_test(mrn, name)

    assert test.mrn == mrn
    assert test.name == name
    assert test.phys_email == "emf55@duke.edu"
    assert test.labemail == "lab@test.com"
    assert test.status == "pending"
    assert (mrn, name) in test_dict
    assert test_dict[(mrn, name)] == test


def test_get_test():
    from test_dict import test_dict, Test, get_test
    test_dict.clear()
    test = Test(
        "hdl",
        "2026-03-21 10:00:00",
        123,
        "doc@test.com",
        "lab@test.com",
        "pending",
        15,
    )
    test_dict[(123, "hdl")] = test
    found = get_test(123, "hdl")
    assert found is not None
    assert found.mrn == 123
    assert found.name == "hdl"
    assert found.age == 15


def test_get_test_none():
    from test_dict import test_dict, get_test
    test_dict.clear()
    assert get_test(123, "hdl") is None
