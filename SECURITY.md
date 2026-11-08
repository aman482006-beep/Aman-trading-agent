# Security policy

## Scope

This is a research and educational codebase. It is not a broker, custodian, portfolio accounting system or production investment-advice service. Portfolio Guardian is a deterministic rules demonstration and must not be relied on as the sole control for real-money decisions.

## Reporting a vulnerability

Please do not open a public issue containing exploit details, credentials, personal data or private financial information. Use GitHub's private vulnerability reporting feature if it is enabled for this repository. Otherwise contact the repository maintainer privately through the contact details on the GitHub profile.

Include the affected path, impact, reproduction steps and any suggested mitigation. Do not include live API keys or real account data.

## Security practices

- Keep credentials in local environment variables; never commit .env files.
- Use least-privilege API keys with spending limits.
- Treat third-party market-data and LLM responses as untrusted input.
- Do not expose broker credentials or tokens in browser code, logs or screenshots.
- Review dependency updates and GitHub Actions permission changes.
