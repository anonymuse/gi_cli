# Wave 1: Foundation and Contracts

Wave 1 establishes a minimal, fixture-backed structure for Factory Fit Profiler as a dual-mode SDLC adaptation agent. It implements the product-spec lifecycle at foundation depth: Assess, Onboard, Retrofit, Automate, Govern, and Scale.

## Architectural Basis

The Wave 1 architecture is governed by the product specification in `docs/product/factory-fit-profiler-product-spec.md` and the canonical architecture diagram in `docs/architecture/diagrams/factory-fit-profiler-architecture.mmd`. Local and server workflows share contracts so that recommendations, generated workflows, and reports remain evidence-backed and auditable.

## Scope

- Shared JSON Schema contracts live in `contracts/`.
- Local workstation command placeholders live behind `sdlc-local`.
- Server-side command placeholders live behind `sdlc-server`.
- Synthetic portfolio-company data starts in `fixtures/synthetic-company/`.
- Smoke tests verify command surfaces are discoverable.
- The architecture diagram mirrors the README and product specification lifecycle so product and engineering documentation remain synchronized.

## Non-goals

- No live DevOps integrations.
- No secret or credential access.
- No deployment orchestration.
- No mutation of remote systems.
