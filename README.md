# Dual-Mode SDLC Adaptation Agent

Fixture-backed MVP skeleton for a Dual-Mode SDLC Adaptation Agent.

## Wave 1 contents

- Shared contracts in `contracts/`.
- Local workstation CLI placeholder: `sdlc-local`.
- Server-side CLI placeholder: `sdlc-server`.
- Synthetic company fixture placeholder in `fixtures/synthetic-company/`.
- Smoke tests in `tests/`.

## Wave 3 server MVP

The server-side vertical slice is fixture-backed and does not connect to live DevOps systems. It supports:

- `sdlc-server inventory --fixture synthetic-company` to classify synthetic portfolio repositories with evidence.
- `sdlc-server blueprints recommend --fixture synthetic-company` to recommend MVP SDLC blueprints.
- `sdlc-server manifest validate <path>` to validate MVP `DeliveryManifest` JSON.
- `sdlc-server manifest compile --target github-actions <path>` to compile a deterministic GitHub Actions workflow.

Example commands:

```bash
PYTHONPATH=src python -m sdlc_adaptation_agent.server_cli inventory --fixture synthetic-company
PYTHONPATH=src python -m sdlc_adaptation_agent.server_cli blueprints recommend --fixture synthetic-company
PYTHONPATH=src python -m sdlc_adaptation_agent.server_cli manifest validate fixtures/synthetic-company/delivery-manifest.valid.json
PYTHONPATH=src python -m sdlc_adaptation_agent.server_cli manifest compile --target github-actions fixtures/synthetic-company/delivery-manifest.valid.json
```

## Development

Run the smoke and Wave 3 tests with:

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```
