from pathlib import Path

from ai_taal.experiment import validate_schemas


def test_json_schemas_are_valid():
    validate_schemas(Path(__file__).resolve().parents[1] / "schemas")

