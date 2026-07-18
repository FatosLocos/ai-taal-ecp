from pathlib import Path

import pytest

from ai_taal.config import load_config


PROJECT_ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="session")
def config():
    return load_config(PROJECT_ROOT / "config" / "ecp0.yaml")


@pytest.fixture(scope="session")
def ecp1_config():
    return load_config(PROJECT_ROOT / "config" / "ecp1.yaml")


@pytest.fixture(scope="session")
def ecp2_config():
    return load_config(PROJECT_ROOT / "config" / "ecp2-development.yaml")


@pytest.fixture(scope="session")
def ecp3_config():
    return load_config(PROJECT_ROOT / "config" / "ecp3.yaml")


@pytest.fixture(scope="session")
def ecp4_config():
    return load_config(PROJECT_ROOT / "config" / "ecp4-development.yaml")


@pytest.fixture(scope="session")
def ecp6_config():
    return load_config(PROJECT_ROOT / "config" / "ecp6-development.yaml")


@pytest.fixture(scope="session")
def ecp7_config():
    return load_config(PROJECT_ROOT / "config" / "ecp7-development.yaml")


@pytest.fixture(scope="session")
def ecp7_positive_control_config():
    return load_config(
        PROJECT_ROOT / "config" / "ecp7-positive-control-development.yaml"
    )


@pytest.fixture(scope="session")
def ecp7_b2_config():
    return load_config(PROJECT_ROOT / "config" / "ecp7-b2-development.yaml")


@pytest.fixture(scope="session")
def ecp7_b3_config():
    return load_config(PROJECT_ROOT / "config" / "ecp7-b3-development.yaml")


@pytest.fixture(scope="session")
def ecp7_b4_config():
    return load_config(PROJECT_ROOT / "config" / "ecp7-b4-development.yaml")


@pytest.fixture(scope="session")
def ecp7_b5_config():
    return load_config(PROJECT_ROOT / "config" / "ecp7-b5-development.yaml")


@pytest.fixture(scope="session")
def ecp7_b6_config():
    return load_config(PROJECT_ROOT / "config" / "ecp7-b6-development.yaml")


@pytest.fixture(scope="session")
def ecp7_b7_config():
    return load_config(PROJECT_ROOT / "config" / "ecp7-b7-development.yaml")


@pytest.fixture(scope="session")
def ecp7_b8_config():
    return load_config(PROJECT_ROOT / "config" / "ecp7-b8-development.yaml")


@pytest.fixture(scope="session")
def ecp7_b9_config():
    return load_config(PROJECT_ROOT / "config" / "ecp7-b9-development.yaml")


@pytest.fixture(scope="session")
def ecp7_b10_config():
    return load_config(PROJECT_ROOT / "config" / "ecp7-b10-development.yaml")


@pytest.fixture(scope="session")
def ecp7_b11_config():
    return load_config(PROJECT_ROOT / "config" / "ecp7-b11-development.yaml")
