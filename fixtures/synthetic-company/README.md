# Synthetic Company Fixture

Fixture-backed portfolio data for Wave 3 Server Agent MVP workflows. The fixture is deterministic and does not connect to live DevOps systems.

## Contents

- `company.json` defines four synthetic repositories:
  - `repo-node-web`: Node.js service with npm and GitHub Actions hints.
  - `repo-python-api`: Python service with Poetry/pytest and GitHub Actions hints.
  - `repo-java-batch`: JVM batch service with Maven and Jenkins hints.
  - `repo-legacy-tools`: low-confidence legacy shell-script repository.
- `delivery-manifest.valid.json` is a valid MVP `DeliveryManifest`.
- `delivery-manifest.invalid.json` intentionally fails validation.

## Demo commands

```bash
PYTHONPATH=src python -m sdlc_adaptation_agent.server_cli inventory --fixture synthetic-company
PYTHONPATH=src python -m sdlc_adaptation_agent.server_cli blueprints recommend --fixture synthetic-company
PYTHONPATH=src python -m sdlc_adaptation_agent.server_cli manifest validate fixtures/synthetic-company/delivery-manifest.valid.json
PYTHONPATH=src python -m sdlc_adaptation_agent.server_cli manifest compile --target github-actions fixtures/synthetic-company/delivery-manifest.valid.json
```
