from copy import deepcopy

import pytest

from ai_taal.config import ConfigError, validate_config
from ai_taal.config import load_config


def test_registered_invariants_are_consistent(config):
    validate_config(config)
    assert config["world"]["meaning_count"] == 1024
    assert config["channel"]["bits_per_message"] == 16


def test_invalid_split_is_rejected(config):
    invalid = deepcopy(config)
    invalid["dataset"]["train_meanings"] -= 1
    with pytest.raises(ConfigError, match="Data splits"):
        validate_config(invalid)


def test_config_can_inherit_and_override_nested_values(tmp_path, config):
    import yaml

    base = tmp_path / "base.yaml"
    child = tmp_path / "child.yaml"
    base.write_text(yaml.safe_dump(config, sort_keys=False), encoding="utf-8")
    child.write_text(
        "extends: base.yaml\ntraining:\n  learning_rate: 0.0005\n",
        encoding="utf-8",
    )

    loaded = load_config(child)

    assert loaded["training"]["learning_rate"] == 0.0005
    assert loaded["training"]["batch_size"] == config["training"]["batch_size"]


def test_frozen_ecp2_arms_differ_only_in_registered_intervention():
    intervention = load_config("config/ecp2.yaml")
    control = load_config("config/ecp2-control.yaml")

    assert intervention["experiment"]["status"] == "frozen_for_confirmatory"
    assert control["experiment"]["status"] == "frozen_for_confirmatory"
    assert intervention["reproducibility"] == control["reproducibility"]
    assert intervention["dataset"] == control["dataset"]
    assert intervention["channel"] == control["channel"]
    assert intervention["agents"] == control["agents"]
    intervention_training = deepcopy(intervention["training"])
    control_training = deepcopy(control["training"])
    intervention_training.pop("slot_binding_consensus")
    control_training.pop("slot_binding_consensus")
    assert intervention_training == control_training


def test_frozen_ecp3_arms_differ_only_in_registered_consensus():
    intervention = load_config("config/ecp3.yaml")
    control = load_config("config/ecp3-control.yaml")

    assert intervention["experiment"]["status"] == "frozen_for_confirmatory"
    assert control["experiment"]["status"] == "frozen_for_confirmatory"
    assert intervention["reproducibility"] == control["reproducibility"]
    assert intervention["dataset"] == control["dataset"]
    assert intervention["channel"] == control["channel"]
    assert intervention["agents"] == control["agents"]
    intervention_training = deepcopy(intervention["training"])
    control_training = deepcopy(control["training"])
    intervention_training.pop("slot_binding_consensus")
    control_training.pop("slot_binding_consensus")
    intervention_training.pop("atom_code_consensus")
    control_training.pop("atom_code_consensus")
    assert intervention_training == control_training


def test_ecp4_channel_is_exactly_at_source_entropy(ecp4_config):
    assert ecp4_config["channel"]["bits_per_symbol_by_factor"] == [3, 3, 2, 2]
    assert ecp4_config["channel"]["bits_per_message"] == 10
    assert ecp4_config["channel"]["bits_per_message"] == ecp4_config["world"][
        "source_entropy_bits"
    ]


def test_ecp6_scales_the_exact_channel_to_fourteen_bits(ecp6_config):
    assert ecp6_config["world"]["meaning_count"] == 16_384
    assert ecp6_config["channel"]["factor_alphabet_sizes"] == [16, 16, 8, 8]
    assert ecp6_config["channel"]["bits_per_symbol_by_factor"] == [4, 4, 3, 3]
    assert ecp6_config["channel"]["bits_per_message"] == 14
    assert ecp6_config["channel"]["bits_per_message"] == ecp6_config["world"][
        "source_entropy_bits"
    ]


def test_ecp7_weakens_structure_without_changing_capacity(
    ecp7_config, ecp7_positive_control_config
):
    assert ecp7_config["world"] == ecp7_positive_control_config["world"]
    assert ecp7_config["dataset"] == ecp7_positive_control_config["dataset"]
    assert ecp7_config["channel"]["type"] == "slot_local_discrete_fixed_length"
    assert ecp7_config["channel"]["slot_alphabet_sizes"] == [16, 16, 8, 8]
    assert ecp7_config["channel"]["bits_per_symbol_by_slot"] == [4, 4, 3, 3]
    assert ecp7_config["channel"]["bits_per_message"] == 14
    assert ecp7_config["agents"]["sender"]["family"] == (
        "bounded_autoregressive_sender"
    )
    assert ecp7_config["agents"]["receiver"]["family"] == (
        "sequence_encoder_multihead_classifier"
    )
    assert ecp7_positive_control_config["agents"]["sender"]["family"] == (
        "minimal_permutation_slot_sender"
    )
    assert ecp7_positive_control_config["channel"]["bits_per_message"] == 14


def test_slot_local_channel_rejects_an_invalid_capacity(ecp7_config):
    invalid = deepcopy(ecp7_config)
    invalid["channel"]["slot_alphabet_sizes"] = [16, 16, 8, 9]
    with pytest.raises(ConfigError, match="bits_per_symbol_by_slot"):
        validate_config(invalid)


def test_slot_local_channel_rejects_too_few_distinct_messages(ecp7_config):
    invalid = deepcopy(ecp7_config)
    invalid["channel"]["slot_alphabet_sizes"] = [15, 16, 8, 8]
    with pytest.raises(ConfigError, match="cannot represent every world meaning"):
        validate_config(invalid)


def test_ecp7_b2_changes_only_factor_agnostic_code_utilization(
    ecp7_config, ecp7_b2_config
):
    assert ecp7_b2_config["world"] == ecp7_config["world"]
    assert ecp7_b2_config["dataset"] == ecp7_config["dataset"]
    assert ecp7_b2_config["channel"] == ecp7_config["channel"]
    assert ecp7_b2_config["agents"] == ecp7_config["agents"]
    assert ecp7_b2_config["training"]["code_utilization"] == {
        "enabled": True,
        "weight": 1.0,
        "warmup_steps": 400,
        "relaxed_temperature": 1.0,
        "independence_weight": 1.0,
    }
    assert ecp7_b2_config["training"]["slot_binding_consensus"]["enabled"] is False
    assert ecp7_b2_config["training"]["atom_code_consensus"]["enabled"] is False


def test_ecp7_b2_rejects_negative_code_utilization_weight(ecp7_b2_config):
    invalid = deepcopy(ecp7_b2_config)
    invalid["training"]["code_utilization"]["weight"] = -0.1
    with pytest.raises(ConfigError, match="Code-utilization weight"):
        validate_config(invalid)


def test_ecp7_b3_changes_only_the_utilization_message_source(
    ecp7_b2_config, ecp7_b3_config
):
    assert ecp7_b3_config["world"] == ecp7_b2_config["world"]
    assert ecp7_b3_config["dataset"] == ecp7_b2_config["dataset"]
    assert ecp7_b3_config["channel"] == ecp7_b2_config["channel"]
    assert ecp7_b3_config["agents"] == ecp7_b2_config["agents"]
    b2_utilization = ecp7_b2_config["training"]["code_utilization"]
    b3_utilization = ecp7_b3_config["training"]["code_utilization"]
    assert b2_utilization == {
        "enabled": True,
        "weight": 1.0,
        "warmup_steps": 400,
        "relaxed_temperature": 1.0,
        "independence_weight": 1.0,
    }
    assert b3_utilization == {
        **b2_utilization,
        "message_source": "straight_through",
    }


def test_ecp7_b3_rejects_an_unknown_message_source(ecp7_b3_config):
    invalid = deepcopy(ecp7_b3_config)
    invalid["training"]["code_utilization"]["message_source"] = "hard_argmax"
    with pytest.raises(ConfigError, match="message_source"):
        validate_config(invalid)
