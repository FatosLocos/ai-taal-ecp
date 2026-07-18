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


@pytest.fixture(scope="session")
def ecp7_b12_config():
    return load_config(PROJECT_ROOT / "config" / "ecp7-b12-development.yaml")


@pytest.fixture(scope="session")
def ecp7_b13_config():
    return load_config(PROJECT_ROOT / "config" / "ecp7-b13-development.yaml")


@pytest.fixture(scope="session")
def ecp7_b14_config():
    return load_config(PROJECT_ROOT / "config" / "ecp7-b14-development.yaml")


@pytest.fixture(scope="session")
def ecp7_b15_config():
    return load_config(PROJECT_ROOT / "config" / "ecp7-b15-development.yaml")


@pytest.fixture(scope="session")
def ecp7_b16_config():
    return load_config(PROJECT_ROOT / "config" / "ecp7-b16-development.yaml")


@pytest.fixture(scope="session")
def ecp7_b17_config():
    return load_config(PROJECT_ROOT / "config" / "ecp7-b17-development.yaml")


@pytest.fixture(scope="session")
def ecp7_b18_config():
    return load_config(PROJECT_ROOT / "config" / "ecp7-b18-development.yaml")


@pytest.fixture(scope="session")
def ecp7_b19_config():
    return load_config(PROJECT_ROOT / "config" / "ecp7-b19-development.yaml")


@pytest.fixture(scope="session")
def ecp7_b20_config():
    return load_config(PROJECT_ROOT / "config" / "ecp7-b20-development.yaml")


@pytest.fixture(scope="session")
def ecp7_b21_config():
    return load_config(PROJECT_ROOT / "config" / "ecp7-b21-development.yaml")


@pytest.fixture(scope="session")
def ecp7_b22_config():
    return load_config(PROJECT_ROOT / "config" / "ecp7-b22-development.yaml")


@pytest.fixture(scope="session")
def ecp7_b23_config():
    return load_config(PROJECT_ROOT / "config" / "ecp7-b23-development.yaml")


@pytest.fixture(scope="session")
def ecp7_b24_config():
    return load_config(PROJECT_ROOT / "config" / "ecp7-b24-development.yaml")


@pytest.fixture(scope="session")
def ecp7_b25_config():
    return load_config(PROJECT_ROOT / "config" / "ecp7-b25-development.yaml")


@pytest.fixture(scope="session")
def ecp7_b26_config():
    return load_config(PROJECT_ROOT / "config" / "ecp7-b26-development.yaml")
