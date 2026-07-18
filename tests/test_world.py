from ai_taal.world import build_splits, enumerate_world, meaning_from_factors


def test_world_ids_round_trip(config):
    world = enumerate_world(config)
    assert len(world) == 1024
    assert world[0].factors == (0, 0, 0, 0)
    assert world[-1].factors == (7, 7, 3, 3)
    for meaning in world:
        assert meaning_from_factors(meaning.factors, config) == meaning


def test_split_is_deterministic_disjoint_and_balanced(config):
    first = build_splits(config)
    second = build_splits(config)
    assert first.manifest() == second.manifest()
    assert (len(first.train), len(first.validation), len(first.compositional_test)) == (
        768,
        128,
        128,
    )
    pairs = first.held_out_color_shape_pairs
    assert len({color for color, _ in pairs}) == 8
    assert len({shape for _, shape in pairs}) == 8
    assert all(
        (meaning.color, meaning.shape) in set(pairs)
        for meaning in first.compositional_test
    )
    assert all(
        (meaning.color, meaning.shape) not in set(pairs)
        for meaning in first.train + first.validation
    )


def test_ecp4_uses_explicit_last_two_matchings(ecp4_config):
    split = build_splits(ecp4_config)
    expected_validation = {
        (0, 4), (1, 5), (2, 7), (3, 3),
        (4, 2), (5, 6), (6, 0), (7, 1),
    }
    expected_test = {
        (0, 7), (1, 1), (2, 2), (3, 4),
        (4, 6), (5, 5), (6, 3), (7, 0),
    }
    assert set(split.held_out_validation_color_shape_pairs) == expected_validation
    assert set(split.held_out_color_shape_pairs) == expected_test


def test_ecp6_scales_world_and_holds_out_only_novel_atomic_pairs(ecp6_config):
    world = enumerate_world(ecp6_config)
    split = build_splits(ecp6_config)

    assert len(world) == 16_384
    assert world[-1].factors == (15, 15, 7, 7)
    assert (len(split.train), len(split.validation), len(split.compositional_test)) == (
        14_336,
        1_024,
        1_024,
    )
    held_out_pairs = (
        split.held_out_validation_color_shape_pairs
        + split.held_out_color_shape_pairs
    )
    assert len(held_out_pairs) == 32
    assert all(color >= 8 or shape >= 8 for color, shape in held_out_pairs)
