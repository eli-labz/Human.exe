from human_exe.workforce.services.roi_calculator import build_roi_scenarios


def test_roi_calculator_generates_three_scenarios() -> None:
    models = build_roi_scenarios(
        baseline_cost=2_000_000,
        implementation_cost=250_000,
        labor_hours_saved=4_000,
        blended_hourly_cost=60,
        quality_gain_percent=0.1,
    )
    names = {model.scenario for model in models}
    assert names == {"conservative", "expected", "aggressive"}
    assert all(model.payback_months > 0 for model in models)
