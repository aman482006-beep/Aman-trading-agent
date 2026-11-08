# Upstream code and attribution

This repository contains two distinct bodies of work. Their ownership and maintenance boundaries should remain explicit.

## Original research experiments

The original work maintained here lives under agent_lab/:

- agent_lab/portfolio_guardian/: deterministic portfolio-risk rules and tests.
- agent_lab/research_copilot/: a deterministic orchestration prototype with illustrative evidence and a rule-based gate.
- agent_lab/earnings_intelligence/: a keyword-overlap retrieval baseline and evidence-linked claim structure.

The current implementations and their limitations are documented in the root README and in the relevant module documentation.

## Upstream TradingAgents component

The tradingagents/ and cli/ directories contain an adapted/retained copy of the TradingAgents framework.

- Upstream project: [Tauric Research / TradingAgents](https://github.com/TauricResearch/TradingAgents)
- Upstream project name: TradingAgents
- Upstream licence: Apache License 2.0
- This repository is not an official Tauric Research repository and is not marked as a GitHub fork.

The upstream component is included for local study, modification and experimentation. Do not attribute the upstream framework's stars, forks, downloads, users, releases or external contributors to this repository or to the original agent_lab/ work.

## Licence and notices

The repository includes an Apache-2.0 licence. Preserve the upstream copyright and attribution notices in retained upstream files when modifying or redistributing them. When making changes under tradingagents/ or cli/, identify those changes clearly in commit messages and pull requests.

For questions about which code is original, use the directory boundary above and inspect the file-level history. A file's presence in this repository does not imply original authorship.
