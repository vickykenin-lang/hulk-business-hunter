# HULK — Credentials Required

HULK never stores secret values in repository files. Provision secrets using GitHub repository Actions secrets.

## Required to activate autonomous research
Provide **at least one** Lead AI credential:

- `AWS_BEDROCK_API_KEY` — preferred if HULK should use the same Bedrock/Qwen-style Lead AI pattern proven in RIO.
- `DEEPSEEK_API_KEY` — supported Lead AI/research fallback credential.
- `OPENAI_API_KEY` — optional alternative provider credential.

## Recommended for resilient multi-model research
Provision both:
- `AWS_BEDROCK_API_KEY`
- `DEEPSEEK_API_KEY`

This allows the runtime to be wired for primary + fallback rather than depending on one provider.

## Not required now
No affiliate, payment, Instagram, advertising, domain, hosting, merchant or customer credentials are required for HULK's research-only mandate. HULK must identify those separately inside each business proposal under **Implementation Requirements & Credential Readiness** if that proposed business would need them.

## Security rule
Never paste secret values into `OBJECTIVE.md`, `SOUL.md`, issues, commits, proposal files, or chat commands intended for logging. Store provider credentials only as repository secrets / an approved secret manager.
