"""Shape B — one ReAct agent. Student work.

Use `lab8.runtime.run_react` with max_steps=8. `decide` may pick a read tool.
It must not call `issue_refund`. After the loop, the host validates the quote
and is the only writer.

A decide() that trusts ticket text over the order row will fail hidden claims
where the customer overstates the delay or cites a superseded clause.

Per-order cap: an order may already have been refunded by an earlier claim.
The read tool `lookup_refund_history` shows how much. The host still enforces
the cap, so pass the full quote to `durability.issue_refund`, not a net amount.

Caps: stop at 8 steps. Count model calls in the Budget so cost stays comparable.

Trace contract v1 (docs/contracts.md): return a trace_path to a JSON file written in this run,
{"run_id": <same run_id>, "events": [...]}, on every return path including early
ones. `lab8.trace.Trace` does this; your own tracer is fine if it matches.
"""

from __future__ import annotations

from lab8.db import connect
from lab8.durability import issue_refund
from lab8.mock_llm import complete
from lab8.runtime import run_react
from lab8.schemas import Budget, RunResult, make_run_id
from lab8.shapes.common import finish
from lab8.tools import get_claim_view, tool_cost
from lab8.trace import Trace


def run_claim(
    claim_id: str,
    *,
    seed: int,
    store_path: str,
    crash_at: str | None = None,
) -> RunResult:
    conn = connect(store_path)
    try:
        budget = Budget()
        trace = Trace(make_run_id("single", claim_id, seed))
        budget.add_tool(tool_cost())
        claim = get_claim_view(conn, claim_id)

        def decide(seen: dict) -> dict:
            # MockLLM records simulated model usage. Its text is not a tool
            # action or a money quote; the adapter below selects read actions.
            last_tool = seen.get("last_tool")
            complete(
                budget, seed=seed, purpose="decide",
                prompt=f"claim_found={claim['found']};last_tool={last_tool}",
            )
            if not claim["found"]:
                return {"final": {"status": "failed", "error_reason": "unknown_claim"}}
            if not claim["order_id"]:
                return {"final": {"status": "needs_info", "error_reason": "missing_order_id"}}

            if last_tool is None:
                trace.add("action", {"tool": "lookup_order"})
                return {
                    "tool": "lookup_order",
                    "args": {
                        "order_id": claim["order_id"],
                        "principal_id": claim["principal_id"],
                    },
                }
            if last_tool == "lookup_order":
                order_view = seen["last_result"]
                trace.add("lookup_order", order_view)
                if not order_view["visible"]:
                    return {"final": {
                        "status": "escalated", "error_reason": order_view["reason"],
                    }}
                trace.add("action", {"tool": "compute_compensation"})
                return {
                    "tool": "compute_compensation",
                    "args": {"order": order_view["order"]},
                }
            if last_tool == "compute_compensation":
                quote = seen["last_result"]
                trace.add("quote", quote)
                return {"final": {"quote": quote}}
            return {"final": {"status": "failed", "error_reason": "unexpected_observation"}}

        reacted = run_react(
            conn, budget, observation={"claim": claim},
            decide=decide, max_steps=8, worker=True,
        )
        final = reacted["final"]
        proposal = 0
        if "quote" not in final:
            status = final["status"]
            error_reason = final.get("error_reason")
        else:
            quote = final["quote"]
            proposal = int(quote["amount_vnd"])
            if proposal <= 0:
                status = "denied"
                error_reason = quote["reason"]
            else:
                # Only host code writes money, after the read-only loop ends.
                # Pass the full quote and let InjectedCrash propagate.
                outcome = issue_refund(conn, claim_id, proposal, crash_at=crash_at)
                if outcome["ok"]:
                    status = "resolved"
                    error_reason = None
                else:
                    status = "failed" if outcome["conflict"] else "denied"
                    error_reason = outcome["reason"]

        trace.add("decision", {"status": status, "reason": error_reason})
        return finish(
            conn, shape="single", claim_id=claim_id, seed=seed,
            status=status, proposal_amount=proposal, budget=budget,
            trace=trace, error_reason=error_reason,
        )
    finally:
        conn.close()
