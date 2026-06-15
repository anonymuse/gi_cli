# Wave 1: Foundation and Contracts

Wave 1 establishes a minimal, fixture-backed structure for the Dual-Mode SDLC Adaptation Agent.

## Scope

- Shared JSON Schema contracts live in `contracts/`.
- Local workstation command placeholders live behind `sdlc-local`.
- Server-side command placeholders live behind `sdlc-server`.
- Synthetic portfolio-company data starts in `fixtures/synthetic-company/`.
- Smoke tests verify command surfaces are discoverable.

## Non-goals

- No live DevOps integrations.
- No secret or credential access.
- No deployment orchestration.
- No mutation of remote systems.
