"""Local Streamlit interface for the original deterministic agent_lab prototypes.

This interface deliberately does not call an LLM, fetch live market data or place trades.
"""
from __future__ import annotations

from dataclasses import asdict

import pandas as pd
import streamlit as st

from agent_lab.earnings_intelligence.pipeline import Chunk, build_claim, retrieve
from agent_lab.portfolio_guardian.risk_engine import Position, evaluate
from agent_lab.research_copilot.core import AgentState, run_research


st.set_page_config(
    page_title="Agentic Finance Research Lab",
    page_icon="AF",
    layout="wide",
)

st.title("Agentic Finance Research Lab")
st.caption("Inspectable finance-agent experiments · deterministic demo mode")

st.info(
    "This local interface uses sample inputs and deterministic prototype code. "
    "It does not call an LLM, fetch live market data, connect to a broker or execute trades."
)

portfolio_tab, research_tab, earnings_tab = st.tabs(
    ["Portfolio Guardian", "Research Copilot", "Earnings Intelligence"]
)

with portfolio_tab:
    st.subheader("Portfolio risk check")
    st.write(
        "Edit the sample positions. Weights are fractions of portfolio value, entered below as "
        "percentages. CASH is excluded from concentration and volatility checks."
    )
    initial_positions = pd.DataFrame(
        [
            {"ticker": "NVDA", "weight_pct": 32.0, "volatility_pct": 58.0},
            {"ticker": "MSFT", "weight_pct": 20.0, "volatility_pct": 31.0},
            {"ticker": "JPM", "weight_pct": 18.0, "volatility_pct": 27.0},
            {"ticker": "CASH", "weight_pct": 30.0, "volatility_pct": 0.0},
        ]
    )
    with st.form("portfolio_form"):
        edited_positions = st.data_editor(
            initial_positions,
            num_rows="dynamic",
            use_container_width=True,
            hide_index=True,
            column_config={
                "ticker": st.column_config.TextColumn("Ticker", required=True),
                "weight_pct": st.column_config.NumberColumn(
                    "Weight (%)", min_value=0.0, max_value=100.0, step=1.0, required=True
                ),
                "volatility_pct": st.column_config.NumberColumn(
                    "Volatility (%)", min_value=0.0, step=1.0, required=True
                ),
            },
        )
        run_portfolio = st.form_submit_button("Evaluate portfolio", type="primary")

    if run_portfolio:
        try:
            positions = []
            for row in edited_positions.to_dict("records"):
                ticker = str(row.get("ticker", "")).strip()
                if not ticker:
                    continue
                positions.append(
                    Position(
                        ticker=ticker,
                        weight=float(row["weight_pct"]) / 100.0,
                        volatility=float(row["volatility_pct"]) / 100.0,
                    )
                )
            report = evaluate(positions)
        except (KeyError, TypeError, ValueError) as exc:
            st.error(f"Input validation failed: {exc}")
        else:
            c1, c2, c3 = st.columns(3)
            c1.metric("Risk score", f"{report.score:.1f} / 100")
            c2.metric("Action", report.action)
            c3.metric("Alerts", len(report.alerts))
            st.markdown("**Scenario losses**")
            st.dataframe(
                pd.DataFrame(
                    [
                        {"scenario": name, "estimated_portfolio_return": f"{loss:.2%}"}
                        for name, loss in report.stress_losses.items()
                    ]
                ),
                hide_index=True,
                use_container_width=True,
            )
            if report.alerts:
                st.markdown("**Alerts**")
                st.dataframe(
                    pd.DataFrame([asdict(alert) for alert in report.alerts]),
                    hide_index=True,
                    use_container_width=True,
                )
            else:
                st.success("No configured risk rules were triggered.")
    st.caption(
        "Heuristic rules only. No covariance, beta, liquidity, drawdown, options or "
        "position-specific scenario model is applied. See SCENARIO_PLAYBOOK.md."
    )

with research_tab:
    st.subheader("Research workflow prototype")
    st.write(
        "This is a deterministic orchestration example with fixed specialist functions and "
        "illustrative evidence. The sample inputs below are not fetched from a financial data source."
    )
    with st.form("research_form"):
        ticker = st.text_input("Ticker", value="DEMO")
        revenue_growth = st.number_input("Revenue growth (%)", value=18.4)
        roic = st.number_input("ROIC (%)", value=21.1)
        debt_to_equity = st.number_input("Debt-to-equity", min_value=0.0, value=0.42)
        fcf_positive = st.selectbox("Free cash flow positive?", [True, False], index=0)
        momentum = st.selectbox("Market momentum", ["positive", "neutral", "negative"])
        volatility = st.number_input("Volatility input (%)", min_value=0.0, value=27.0)
        run_research_button = st.form_submit_button("Run deterministic workflow", type="primary")

    if run_research_button:
        try:
            state = AgentState(
                question=f"Is {ticker.strip().upper()} worth researching further?",
                ticker=ticker.strip().upper(),
                facts={
                    "revenue_growth_pct": revenue_growth,
                    "roic_pct": roic,
                    "free_cash_flow_positive": fcf_positive,
                    "debt_to_equity": debt_to_equity,
                    "momentum": momentum,
                    "volatility_pct": volatility,
                },
            )
            result = run_research(state)
        except (TypeError, ValueError) as exc:
            st.error(f"Input validation failed: {exc}")
        else:
            st.metric("Risk gate", result.outputs["risk_gate"])
            st.write(result.outputs["synthesis"])
            left, right = st.columns(2)
            with left:
                st.markdown("**Illustrative evidence ledger**")
                st.dataframe(
                    pd.DataFrame([asdict(item) for item in result.evidence]),
                    hide_index=True,
                    use_container_width=True,
                )
            with right:
                st.markdown("**Execution trace**")
                st.json(result.trace)
            if result.vetoes:
                st.warning("Vetoes: " + "; ".join(result.vetoes))

with earnings_tab:
    st.subheader("Earnings Intelligence retrieval baseline")
    st.write(
        "A small lexical retrieval demonstration over supplied text chunks. It uses token overlap, "
        "not embeddings or an external document source."
    )
    sample_chunks = [
        Chunk(
            "Q1-guidance",
            "Management expects cloud revenue growth to remain above 20 percent.",
            "guidance",
        ),
        Chunk(
            "Q1-margin",
            "Operating margin expanded by 180 basis points year over year.",
            "financials",
        ),
        Chunk(
            "Q1-risk",
            "Management highlighted elevated customer acquisition costs as a near-term risk.",
            "risks",
        ),
    ]
    query = st.text_input("Search the sample transcript", value="revenue growth guidance")
    if st.button("Retrieve evidence", type="primary"):
        try:
            evidence = retrieve(sample_chunks, query)
            claim = build_claim(
                "The supplied excerpts indicate a growth outlook that should be reviewed "
                "alongside operating and acquisition-cost risks.",
                evidence,
            )
        except (TypeError, ValueError) as exc:
            st.error(f"Retrieval input failed: {exc}")
        else:
            st.markdown("**Illustrative claim**")
            st.write(claim.text)
            st.metric(
                "Heuristic confidence",
                f"{claim.confidence:.2f}",
                help="A simple evidence-count heuristic; it is not statistically calibrated.",
            )
            if evidence:
                st.dataframe(
                    pd.DataFrame(
                        [
                            {"evidence_id": item.id, "section": item.section, "text": item.text}
                            for item in evidence
                        ]
                    ),
                    hide_index=True,
                    use_container_width=True,
                )
            else:
                st.warning("No sample text matched the query.")

st.divider()
st.caption(
    "Research and educational software only. Outputs are not investment advice, "
    "not a suitability assessment and not an instruction to buy or sell any security."
)
