# GAUSS AI Agent Network – Integration Guide

## What is implemented

- Flask API and dashboard for the central agent network.
- Agent catalog for Quantum KI Ultra Pro, IONOS, Galactic AI, Quantum Mirror, Quantenformel, Note-KI, Quantumlight and Cat Chat.
- Provider adapters use only explicitly configured HTTPS endpoints; unconfigured providers are shown as offline.
- Task records are stored in SQLite.
- Update proposals require an admin key and are stored as awaiting human approval.
- A small embeddable site widget is available at `/static/gauss-agent.js`.
- Weekly CI runs compile checks, tests and dependency audits; Dependabot proposes dependency updates.

## Deploy

Use the Render Blueprint in `render.yaml`. Set these secrets in Render:
- `THE_LORD_ADMIN_API_KEY`: a long random value, generated in a password manager.
- `THE_LORD_AI_PROVIDERS`: JSON mapping agent IDs to your real HTTPS API endpoints.
- Any provider key environment variables referenced by `api_key_env`.

The example file `agent-providers.example.json` is documentation only. Do not copy placeholder URLs into production.

## Add the agent widget to an eligible website

After the central service is deployed, add this before `</body>`:

```html
<script src="https://YOUR-THE-LORD-URL/static/gauss-agent.js"
        data-api-base="https://YOUR-THE-LORD-URL" defer></script>
```

Do not add it to Rothshild, Lyca, Parfum, Sneaker or any webshop unless the owner explicitly changes that exclusion.

## Agent and update safety

- Provider calls are outbound HTTPS POST requests only to endpoints configured by the operator.
- Never expose provider credentials in browser JavaScript.
- Never let an agent run arbitrary shell commands or deploy arbitrary code.
- Scheduled CI audits and Dependabot pull requests are automatic; production deployments and code changes require review and explicit approval.
- The current adapter sends a generic JSON payload containing `message`, `prompt`, `context` and `agent`. Each legacy AI may need a small adapter to match its exact API contract.
- Use a managed PostgreSQL database instead of SQLite if multiple web instances or higher write concurrency are needed.
