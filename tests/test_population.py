from ai_taal.models import ModelSpec, PopulationSystem
from ai_taal.training import evaluate_population, meanings_tensor, train_population_system
from ai_taal.world import build_splits


ECP0_TEST_PAIRS = {
    (0, 3),
    (1, 0),
    (2, 4),
    (3, 1),
    (4, 5),
    (5, 2),
    (6, 6),
    (7, 7),
}


def test_ecp1_split_excludes_every_ecp0_test_pair(ecp1_config):
    split = build_splits(ecp1_config)
    assert set(split.held_out_color_shape_pairs).isdisjoint(ECP0_TEST_PAIRS)
    assert len(split.compositional_test) == 128


def test_population_has_independent_parameters(ecp1_config):
    population = PopulationSystem(
        ModelSpec.from_config(ecp1_config), sender_count=4, receiver_count=4
    )
    parameter_ids = [
        {id(parameter) for parameter in agent.parameters()}
        for agent in list(population.senders) + list(population.receivers)
    ]
    for left in range(len(parameter_ids)):
        for right in range(left + 1, len(parameter_ids)):
            assert parameter_ids[left].isdisjoint(parameter_ids[right])


def test_population_smoke_training_completes(ecp1_config):
    split = build_splits(ecp1_config)
    population, result = train_population_system(
        ecp1_config,
        split.train,
        split.validation,
        seed=11,
        max_steps_override=2,
    )
    metrics = evaluate_population(population, meanings_tensor(split.validation[:8]))
    assert result.best_step in {1, 2}
    assert len(metrics["pairs"]) == 16
    assert 0.0 <= metrics["worst_pair_exact_match"] <= metrics["mean_exact_match"]


def test_ecp2_uses_disjoint_compositional_validation_and_test_matchings(ecp2_config):
    split = build_splits(ecp2_config)
    validation_pairs = set(split.held_out_validation_color_shape_pairs)
    test_pairs = set(split.held_out_color_shape_pairs)
    excluded = {
        (pair["color"], pair["shape"])
        for pair in ecp2_config["dataset"]["excluded_color_shape_pairs"]
    }

    assert len(validation_pairs) == len(test_pairs) == 8
    assert validation_pairs.isdisjoint(test_pairs | excluded)
    assert test_pairs.isdisjoint(excluded)
    assert {(meaning.color, meaning.shape) for meaning in split.validation} == validation_pairs
    assert {
        (meaning.color, meaning.shape) for meaning in split.compositional_test
    } == test_pairs
    assert all(
        (meaning.color, meaning.shape) not in validation_pairs | test_pairs
        for meaning in split.train
    )


def test_cultural_transmission_requires_a_full_turnover_before_selection(ecp2_config):
    config = deepcopy(ecp2_config)
    config["agents"]["population"].update(sender_count=2, receiver_count=2)
    config["training"].update(
        evaluation_interval=1,
        minimum_steps=1,
        patience_steps=10,
    )
    config["training"]["algebraic_consistency"]["enabled"] = False
    config["training"]["cultural_transmission"].update(
        enabled=True,
        replacement_interval=2,
        minimum_full_turnovers=1,
    )
    split = build_splits(config)

    _, result = train_population_system(
        config,
        split.train,
        split.validation,
        seed=11,
        max_steps_override=5,
    )

    assert result.best_step == 5
    assert result.history[-1]["replacement_count"] == 2
    assert result.history[-1]["full_population_turnovers"] == 1.0
from copy import deepcopy
