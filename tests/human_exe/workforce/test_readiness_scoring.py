from human_exe.workforce.services.readiness_scoring import score_readiness


def test_readiness_scoring_maps_to_levels() -> None:
    low = score_readiness(0.1, 0.1, 0.2, 0.2, 0.2, 0.1, 0.1)
    high = score_readiness(0.85, 0.8, 0.82, 0.88, 0.9, 0.86, 0.84)

    assert low.level.startswith("Level 0") or low.level.startswith("Level 1")
    assert high.level.startswith("Level 5")
    assert high.overall > low.overall
