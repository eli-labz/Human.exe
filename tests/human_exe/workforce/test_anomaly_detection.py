from human_exe.workforce.models.company import EmployeeAggregate, SkillProfile
from human_exe.workforce.models.workflow import SystemProfile, TaskProfile, WorkflowProfile
from human_exe.workforce.services.anomaly_detection import detect_anomalies


def test_anomaly_detection_returns_ranked_findings() -> None:
    employees = [
        EmployeeAggregate("R1", 10, 40, 0.1, 120, 0.04),
        EmployeeAggregate("R2", 10, 44, 0.32, 420, 0.09),
        EmployeeAggregate("R3", 10, 39, 0.08, 90, 0.02),
    ]
    tasks = [
        TaskProfile("T1", "R2", "W1", "data entry", "ops", 420, 22, 0.12, 0.3, 4, False, True),
    ]
    workflows = [
        WorkflowProfile("W1", "D1", "R2", ["R2"], "Core", ["ERP", "Email"], 58, 260, 4, 0.2, 6),
    ]
    skills = [SkillProfile("AI", "R2", 0.8, 0.35, 0.4)]
    systems = [SystemProfile("S1", "ERP", "ERP", ["D1"], 0.8, 0.35)]

    findings = detect_anomalies(employees, tasks, workflows, skills, systems)
    assert findings
    assert any(f.category == "workload" for f in findings)
    assert any(f.category == "process" for f in findings)
    assert any(f.category == "skills" for f in findings)
