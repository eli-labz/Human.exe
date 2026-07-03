"""End-to-end supervised computer-use flow for demo workflow."""

from __future__ import annotations

from pathlib import Path
from time import perf_counter
from uuid import uuid4

from human_exe.crews.digital_labor_crew import DigitalLaborCrew
from human_exe.flows.approval_flow import run_supervised_approval_flow
from human_exe.flows.recovery_flow import run_recovery_flow
from human_exe.flows.text_task_flow import run_text_task_flow
from human_exe.models.metrics import CognitiveDebtIndex, ReliabilityMetrics
from human_exe.models.supervision import ApprovalRequest
from human_exe.models.tokens import ActionType, HumanActionToken, IntentToken, OutcomeToken
from human_exe.models.workflow import WorkflowTrace
from human_exe.observability.reliability_report import generate_reliability_report
from human_exe.policy.risk_engine import AllocationInputs, compute_ai_share, compute_risk_score
from human_exe.tools.file_tools import FileAdapter
from human_exe.tools.verification_tools import verify_non_empty_text


def run_browser_task_flow() -> dict[str, object]:
    return {"status": "sandboxed", "flow": "browser_task_flow"}


def run_desktop_task_flow() -> dict[str, object]:
    return {"status": "sandboxed", "flow": "desktop_task_flow"}


def run_file_task_flow(path: Path) -> dict[str, object]:
    file_adapter = FileAdapter()
    content = file_adapter.read_file(path)
    return {"status": "ok", "length": len(content)}


def run_audit_log_flow() -> dict[str, object]:
    return {"status": "ok", "flow": "audit_log_flow"}


def run_demo_workflow(
    document_path: Path,
    recipient: str,
    supervisor_id: str = "supervisor-1",
    artifacts_root: Path = Path(".artifacts/human_exe"),
) -> dict[str, object]:
    started = perf_counter()
    workflow_id = str(uuid4())
    crew = DigitalLaborCrew(artifacts_root=artifacts_root)
    file_adapter = FileAdapter()

    intent = IntentToken(
        task_id=workflow_id,
        objective="Summarize local document and prepare supervised email draft",
        business_goal="Reduce repetitive reporting workload with supervised digital labor",
        created_by="human-supervisor",
    )

    trace = WorkflowTrace(
        workflow_id=workflow_id,
        intent=intent,
        context={"document_path": str(document_path), "recipient": recipient},
    )
    crew.supervision.audit_logger.log("intent_created", {"workflow_id": workflow_id, "objective": intent.objective})

    plan = crew.planner.plan(intent.objective)
    trace.context["plan"] = plan

    perception = crew.computer_crew.computer_agent.observe(workflow_id)
    trace.perceptions.append(perception)

    document_text = file_adapter.read_file(document_path)
    text_result = run_text_task_flow(content=document_text, recipient=recipient)
    summary = str(text_result["summary"])
    draft_email = str(text_result["draft"])

    draft_verification = verify_non_empty_text(draft_email)
    trace.verification_results.append(draft_verification)

    action = HumanActionToken(
        task_id=workflow_id,
        action_type=ActionType.SEND_DRAFT_FOR_APPROVAL,
        parameters={"recipient": recipient, "draft": draft_email},
        actor="computer_use_agent",
    )
    trace.actions.append(action)
    crew.supervision.audit_logger.log(
        "action_created",
        {"workflow_id": workflow_id, "action_type": action.action_type.value, "action_id": action.token_id},
    )

    allocation_inputs = AllocationInputs(
        repeatability=0.85,
        task_maturity=0.80,
        historical_success_rate=0.82,
        action_reversibility=0.92,
        data_sensitivity=0.40,
        business_risk=0.42,
        human_approval_requirement=0.80,
        observed_ui_stability=0.75,
        recovery_reliability=0.74,
    )
    risk_score = compute_risk_score(allocation_inputs)
    ai_share = compute_ai_share(allocation_inputs)
    risk_assessment = crew.risk_gate.assess(action, risk_score=risk_score, threshold=0.65)
    trace.context["ai_share"] = ai_share
    trace.context["risk_score"] = risk_score
    trace.context["risk_reasons"] = risk_assessment.reasons

    approval_request = ApprovalRequest(
        workflow_id=workflow_id,
        action={"type": action.action_type.value, "parameters": action.parameters},
        risk_score=risk_score,
        reason="Draft preparation completed. Human approval required before send/export.",
    )
    decision = run_supervised_approval_flow(crew.supervision, approval_request, supervisor_id=supervisor_id)
    trace.supervisor_decisions.append({
        "request_id": decision.request_id,
        "decision": decision.decision.value,
        "reason": decision.reason,
    })
    outcome = OutcomeToken(
        task_id=workflow_id,
        action_token_id=action.token_id,
        success=decision.decision.value != "REJECT",
        verification_passed=True,
        result={"decision": decision.decision.value},
    )
    trace.outcomes.append(outcome)
    crew.supervision.audit_logger.log(
        "outcome_recorded",
        {"workflow_id": workflow_id, "action_id": action.token_id, "success": outcome.success},
    )

    if decision.decision.value == "REJECT":
        trace.final_status = "REJECTED"
        trace.failure_reason = "Supervisor rejected draft"
        trace.recovery_path = run_recovery_flow(trace.failure_reason)["steps"]
    else:
        draft_path = file_adapter.create_document(artifacts_root / "drafts" / f"{workflow_id}.txt", draft_email)
        trace.context["draft_path"] = str(draft_path)
        trace.final_status = "COMPLETED"

    trace_path = crew.memory.save(trace)

    duration = perf_counter() - started
    metrics = ReliabilityMetrics(
        task_completion_rate=1.0 if trace.final_status == "COMPLETED" else 0.0,
        action_success_rate=1.0,
        verification_success_rate=1.0 if draft_verification["passed"] else 0.0,
        recovery_rate=0.0,
        escalation_rate=0.0,
        policy_violation_rate=0.0,
        human_override_rate=0.0,
        time_to_useful_result=duration,
        approval_latency=0.0,
        repeated_failure_count=0,
    )
    cognitive_debt = CognitiveDebtIndex(
        review_depth=0.7,
        override_frequency=0.2,
        approval_speed=0.4,
        escalation_quality=0.8,
        ability_to_complete_without_agent=0.7,
        strategic_engagement=0.75,
    )
    report = generate_reliability_report(
        metrics,
        cognitive_debt,
        artifacts_root / "reports" / f"{workflow_id}_reliability.json",
    )
    crew.supervision.audit_logger.log("workflow_finalized", {"workflow_id": workflow_id, "status": trace.final_status})

    return {
        "workflow_id": workflow_id,
        "summary": summary,
        "draft_email": draft_email,
        "trace_path": str(trace_path),
        "reliability_report": report,
        "ai_share": ai_share,
    }
