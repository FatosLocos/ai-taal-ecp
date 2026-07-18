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


def test_ecp7_b4_adds_only_direct_joint_collision_pressure(
    ecp7_b3_config, ecp7_b4_config
):
    assert ecp7_b4_config["world"] == ecp7_b3_config["world"]
    assert ecp7_b4_config["dataset"] == ecp7_b3_config["dataset"]
    assert ecp7_b4_config["channel"] == ecp7_b3_config["channel"]
    assert ecp7_b4_config["agents"] == ecp7_b3_config["agents"]
    assert (
        ecp7_b4_config["training"]["code_utilization"]
        == ecp7_b3_config["training"]["code_utilization"]
    )
    assert ecp7_b4_config["training"]["joint_message_collision"] == {
        "enabled": True,
        "weight": 1.0,
        "warmup_steps": 400,
    }


def test_ecp7_b4_rejects_negative_joint_collision_weight(ecp7_b4_config):
    invalid = deepcopy(ecp7_b4_config)
    invalid["training"]["joint_message_collision"]["weight"] = -0.1
    with pytest.raises(ConfigError, match="Joint-collision weight"):
        validate_config(invalid)


def test_ecp7_b5_adds_only_sender_message_consensus(
    ecp7_b3_config, ecp7_b5_config
):
    assert ecp7_b5_config["world"] == ecp7_b3_config["world"]
    assert ecp7_b5_config["dataset"] == ecp7_b3_config["dataset"]
    assert ecp7_b5_config["channel"] == ecp7_b3_config["channel"]
    assert ecp7_b5_config["agents"] == ecp7_b3_config["agents"]
    assert (
        ecp7_b5_config["training"]["code_utilization"]
        == ecp7_b3_config["training"]["code_utilization"]
    )
    assert "joint_message_collision" not in ecp7_b5_config["training"]
    assert ecp7_b5_config["training"]["sender_message_consensus"] == {
        "enabled": True,
        "weight": 1.0,
        "warmup_steps": 400,
    }


def test_ecp7_b5_rejects_invalid_sender_consensus_parameters(ecp7_b5_config):
    invalid_weight = deepcopy(ecp7_b5_config)
    invalid_weight["training"]["sender_message_consensus"]["weight"] = -0.1
    with pytest.raises(ConfigError, match="Sender-message consensus weight"):
        validate_config(invalid_weight)

    invalid_warmup = deepcopy(ecp7_b5_config)
    invalid_warmup["training"]["sender_message_consensus"]["warmup_steps"] = 0
    with pytest.raises(ConfigError, match="Sender-message consensus warmup"):
        validate_config(invalid_warmup)


def test_ecp7_b6_adds_only_normalized_factor_minimax(
    ecp7_b3_config, ecp7_b6_config
):
    assert ecp7_b6_config["world"] == ecp7_b3_config["world"]
    assert ecp7_b6_config["dataset"] == ecp7_b3_config["dataset"]
    assert ecp7_b6_config["channel"] == ecp7_b3_config["channel"]
    assert ecp7_b6_config["agents"] == ecp7_b3_config["agents"]
    assert (
        ecp7_b6_config["training"]["code_utilization"]
        == ecp7_b3_config["training"]["code_utilization"]
    )
    assert "joint_message_collision" not in ecp7_b6_config["training"]
    assert "sender_message_consensus" not in ecp7_b6_config["training"]
    assert ecp7_b6_config["training"]["factor_minimax"] == {
        "enabled": True,
        "weight": 1.0,
        "warmup_steps": 400,
    }


def test_ecp7_b6_rejects_invalid_factor_minimax_parameters(ecp7_b6_config):
    invalid_weight = deepcopy(ecp7_b6_config)
    invalid_weight["training"]["factor_minimax"]["weight"] = -0.1
    with pytest.raises(ConfigError, match="Factor-minimax weight"):
        validate_config(invalid_weight)

    invalid_warmup = deepcopy(ecp7_b6_config)
    invalid_warmup["training"]["factor_minimax"]["warmup_steps"] = 0
    with pytest.raises(ConfigError, match="Factor-minimax warmup"):
        validate_config(invalid_warmup)


def test_ecp7_b7_changes_only_the_sender_generation_architecture(
    ecp7_b3_config, ecp7_b7_config
):
    assert ecp7_b7_config["world"] == ecp7_b3_config["world"]
    assert ecp7_b7_config["dataset"] == ecp7_b3_config["dataset"]
    assert ecp7_b7_config["channel"] == ecp7_b3_config["channel"]
    assert (
        ecp7_b7_config["agents"]["receiver"]
        == ecp7_b3_config["agents"]["receiver"]
    )
    assert (
        ecp7_b7_config["agents"]["translator"]
        == ecp7_b3_config["agents"]["translator"]
    )
    assert ecp7_b7_config["agents"]["sender"] == {
        "family": "bounded_parallel_sender"
    }
    b3_training = deepcopy(ecp7_b3_config["training"])
    b7_training = deepcopy(ecp7_b7_config["training"])
    assert b3_training.pop("discrete_estimator") == (
        "straight_through_bounded_autoregressive"
    )
    assert (
        b7_training.pop("discrete_estimator")
        == "straight_through_bounded_parallel"
    )
    assert b7_training == b3_training
    assert "joint_message_collision" not in b7_training
    assert "sender_message_consensus" not in b7_training
    assert "factor_minimax" not in b7_training


def test_ecp7_b8_adds_only_algebraic_context_invariance(
    ecp7_b7_config, ecp7_b8_config
):
    assert ecp7_b8_config["world"] == ecp7_b7_config["world"]
    assert ecp7_b8_config["dataset"] == ecp7_b7_config["dataset"]
    assert ecp7_b8_config["channel"] == ecp7_b7_config["channel"]
    assert ecp7_b8_config["agents"] == ecp7_b7_config["agents"]
    b7_training = deepcopy(ecp7_b7_config["training"])
    b8_training = deepcopy(ecp7_b8_config["training"])
    assert b7_training.pop("algebraic_consistency") == {
        "enabled": False,
        "weight": 0.0,
        "warmup_steps": 800,
        "relaxed_temperature": 1.0,
        "batch_size": 32,
        "quadruple_pool_size": 8192,
    }
    assert b8_training.pop("algebraic_consistency") == {
        "enabled": True,
        "weight": 1.0,
        "warmup_steps": 800,
        "relaxed_temperature": 1.0,
        "batch_size": 32,
        "quadruple_pool_size": 8192,
    }
    assert b8_training == b7_training
    assert "joint_message_collision" not in b8_training
    assert "sender_message_consensus" not in b8_training
    assert "factor_minimax" not in b8_training


def test_ecp7_b9_changes_only_the_shared_decoder_family(
    ecp7_b7_config, ecp7_b9_config
):
    assert ecp7_b9_config["world"] == ecp7_b7_config["world"]
    assert ecp7_b9_config["dataset"] == ecp7_b7_config["dataset"]
    assert ecp7_b9_config["channel"] == ecp7_b7_config["channel"]
    assert ecp7_b9_config["training"] == ecp7_b7_config["training"]
    assert (
        ecp7_b9_config["agents"]["sender"]
        == ecp7_b7_config["agents"]["sender"]
    )
    assert (
        ecp7_b9_config["agents"]["population"]
        == ecp7_b7_config["agents"]["population"]
    )
    assert ecp7_b9_config["agents"]["receiver"] == {
        "family": "position_aware_mlp_receiver"
    }
    b7_translator = deepcopy(ecp7_b7_config["agents"]["translator"])
    b9_translator = deepcopy(ecp7_b9_config["agents"]["translator"])
    assert b7_translator.pop("family") == "sequence_encoder_multihead_classifier"
    assert b9_translator.pop("family") == "position_aware_mlp_receiver"
    assert b9_translator == b7_translator


def test_ecp7_b10_changes_only_the_population_optimization_horizon(
    ecp7_b9_config, ecp7_b10_config
):
    assert ecp7_b10_config["world"] == ecp7_b9_config["world"]
    assert ecp7_b10_config["dataset"] == ecp7_b9_config["dataset"]
    assert ecp7_b10_config["channel"] == ecp7_b9_config["channel"]
    assert ecp7_b10_config["agents"] == ecp7_b9_config["agents"]
    b9_training = deepcopy(ecp7_b9_config["training"])
    b10_training = deepcopy(ecp7_b10_config["training"])
    assert b9_training.pop("max_steps") == 5000
    assert b10_training.pop("max_steps") == 15000
    assert b9_training.pop("minimum_steps") == 2000
    assert b10_training.pop("minimum_steps") == 5000
    assert b9_training.pop("patience_steps") == 1600
    assert b10_training.pop("patience_steps") == 3000
    assert b10_training.pop("temperature_schedule_steps") == 5000
    assert b10_training == b9_training


def test_temperature_schedule_steps_must_fit_the_training_horizon(
    ecp7_b10_config,
):
    invalid_type = deepcopy(ecp7_b10_config)
    invalid_type["training"]["temperature_schedule_steps"] = 1.5
    with pytest.raises(ConfigError, match="integer of at least 2"):
        validate_config(invalid_type)

    invalid_short = deepcopy(ecp7_b10_config)
    invalid_short["training"]["temperature_schedule_steps"] = 1
    with pytest.raises(ConfigError, match="integer of at least 2"):
        validate_config(invalid_short)

    invalid_long = deepcopy(ecp7_b10_config)
    invalid_long["training"]["temperature_schedule_steps"] = 15001
    with pytest.raises(ConfigError, match="cannot exceed max_steps"):
        validate_config(invalid_long)


def test_ecp7_b11_changes_only_the_code_utilization_weight_schedule(
    ecp7_b10_config, ecp7_b11_config
):
    assert ecp7_b11_config["world"] == ecp7_b10_config["world"]
    assert ecp7_b11_config["dataset"] == ecp7_b10_config["dataset"]
    assert ecp7_b11_config["channel"] == ecp7_b10_config["channel"]
    assert ecp7_b11_config["agents"] == ecp7_b10_config["agents"]
    b10_training = deepcopy(ecp7_b10_config["training"])
    b11_training = deepcopy(ecp7_b11_config["training"])
    assert b11_training["code_utilization"].pop("weight_decay") == {
        "enabled": True,
        "start_step": 5000,
        "end_step": 15000,
        "final_weight": 0.1,
    }
    assert b11_training == b10_training


def test_code_utilization_weight_decay_must_be_bounded(ecp7_b11_config):
    before_warmup = deepcopy(ecp7_b11_config)
    before_warmup["training"]["code_utilization"]["weight_decay"][
        "start_step"
    ] = 399
    with pytest.raises(ConfigError, match="before warmup"):
        validate_config(before_warmup)

    after_training = deepcopy(ecp7_b11_config)
    after_training["training"]["code_utilization"]["weight_decay"][
        "end_step"
    ] = 15001
    with pytest.raises(ConfigError, match="fit max_steps"):
        validate_config(after_training)

    excessive_final = deepcopy(ecp7_b11_config)
    excessive_final["training"]["code_utilization"]["weight_decay"][
        "final_weight"
    ] = 1.0
    with pytest.raises(ConfigError, match="below its initial weight"):
        validate_config(excessive_final)
