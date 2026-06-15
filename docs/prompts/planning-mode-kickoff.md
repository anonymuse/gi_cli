# Dual-Mode SDLC Adaptation Agent: Planning-Mode Kickoff Prompt

Use this prompt to start **planning mode** for the Dual-Mode SDLC Adaptation Agent.

## Role

You are the planning lead for a product and engineering effort to build a two-mode SDLC improvement product for a private-equity portfolio-company context.

The product is not merely an SDLC factory. It is the diagnostic, adaptation, onboarding, governance, and automation layer that determines how an SDLC factory should be applied to real companies with legacy systems, uneven documentation, fragmented DevOps tooling, manual processes, inherited architectures, vendor constraints, security requirements, and business obligations that cannot pause for modernization.

## Product Concept

The product is a **Dual-Mode SDLC Adaptation Agent** with two execution modes:

1. **Local Workstation Agent**
   - Runs on a developer laptop under explicit user control.
   - Interacts with the IDE, terminal, filesystem, and operating system only within policy boundaries.
   - Helps onboard a developer into agentic coding practices.
   - Guides the developer to a first safe commit.
   - Teaches human-led AI coding, constrained autonomous coding, and agent harness creation.
   - Helps create evals to measure SDLC agent output quality.

2. **Server-Side SDLC Agent**
   - Runs as a containerized service.
   - Connects read-only to DevOps ecosystem APIs in later versions.
   - For MVP, operates against fixtures and synthetic portfolio-company data.
   - Inventories repositories, build systems, CI/CD tools, artifact systems, scanners, and deployment patterns.
   - Classifies build types and delivery patterns.
   - Identifies standardization opportunities.
   - Recommends reusable SDLC blueprints.
   - Abstracts heterogeneous build systems into a simplified user-defined `DeliveryManifest`.

The two modes share the same domain model, schemas, policy controls, evidence model, trace model, eval model, blueprint catalog, and reporting system.

## Strategic Thesis

There is no pure greenfield portfolio company.

A generic SDLC factory risks imposing standardization before understanding the estate. A better private-equity operating capability is:

```text
Assess → Onboard → Retrofit → Automate → Govern → Scale
```

The local agent proves that individual developers can be guided into agentic SDLC practices.

The server agent proves that portfolio-company delivery ecosystems can be inventoried, classified, standardized, and abstracted without pretending they are clean-room environments.

Together, the product becomes the adaptation layer for applying an SDLC factory to real companies.

## Planning-Mode Instructions

This is a planning-mode prompt.

Do **not** write implementation code yet.

First inspect the current repository structure and existing conventions. Do not assume the repository is empty. Prefer incremental integration over replacement.

Produce an implementation-ready plan with the following sections:

1. Product interpretation
2. MVP scope boundary
3. Explicit MVP non-goals
4. Proposed repository structure
5. Core packages and responsibilities
6. Local CLI command surface
7. Server CLI command surface
8. Domain model outline
9. Evidence, trace, policy, and eval contracts
10. `DeliveryManifest` MVP schema outline
11. Synthetic fixture and demo design
12. Recombined agent execution waves
13. File and directory ownership by implementation agent
14. Dependency graph between workstreams
15. Acceptance criteria for the first runnable demo
16. Risks, assumptions, and open questions
17. Recommended first implementation task

Prefer a narrow vertical slice over broad platform design.

## MVP Non-Goals

The MVP will not:

- Connect to live enterprise DevOps systems.
- Mutate remote DevOps platforms.
- Push code to remotes.
- Open production pull requests.
- Install system dependencies automatically.
- Support every language, framework, or CI provider.
- Implement live deployment orchestration.
- Implement unrestricted desktop automation.
- Read secrets, credential stores, SSH config, or private environment files.
- Modify `.env`, key files, credential stores, or global system configuration.

## First Thin Slice

The first runnable demo should prove only:

1. `sdlc-local doctor` can inspect a fixture or local repository and produce structured findings.
2. `sdlc-local explain` can summarize repository purpose, build hints, and safe first-change suggestions.
3. `sdlc-local harness create` can generate a minimal local agent harness with policy gates and validation hooks.
4. `sdlc-local eval patch-quality` can score a sample patch using a repeatable rubric.
5. `sdlc-server inventory --fixture synthetic-company` can classify repositories from fixture data.
6. `sdlc-server blueprints recommend` can recommend standardization blueprints with evidence.
7. `sdlc-server manifest validate` can validate one `DeliveryManifest`.
8. `sdlc-server manifest compile --target github-actions` can emit one GitHub Actions workflow.

All external DevOps integrations should be mocked or fixture-based in the MVP.

## Local Agent Action Policy

Allowed without approval:

- Read repository files.
- Inspect Git status.
- Run configured read-only commands.
- Generate reports.
- Propose patches.

Requires explicit approval:

- Modifying files.
- Running package managers.
- Creating commits.
- Deleting files.
- Changing permissions.
- Writing outside the repository.

Forbidden in MVP:

- Pushing to remotes.
- Changing global system config.
- Reading secrets or credential stores.
- Modifying `.env`, private key files, SSH config, or credential stores.
- Executing arbitrary downloaded scripts.

## Evidence Model Contract

Every classification, recommendation, eval finding, and report claim should cite evidence.

Evidence records should include:

- `id`
- `source_type`: `file`, `command`, `api`, `fixture`, or `user_input`
- `source_location`: path, URL, command, fixture id, or user-provided context id
- `observed_value`
- `timestamp`
- `confidence`
- `related_finding_id`

## Eval Contract

Initial eval type: `patch_quality`.

Eval dimensions:

- correctness
- buildability
- minimality
- safety
- explainability
- evidence use
- policy compliance

Each dimension should be scored from 0 to 2:

- `0`: fail
- `1`: partial or inconclusive
- `2`: pass

Critical dimensions:

- correctness
- buildability
- safety
- policy compliance

Overall status:

- `pass` if all critical dimensions score 2 and total score is at least 12.
- `fail` if any critical dimension scores 0.
- `inconclusive` otherwise.

## DeliveryManifest MVP Scope

For MVP, `DeliveryManifest` supports only:

- Project identity.
- Runtime language and version.
- Install command.
- Build command.
- Test command.
- Optional scan command.
- Optional package/container metadata.
- Evidence output declarations.

Deployment modeling should be represented as a placeholder but not fully implemented.

## Target Case-Study Positioning

The final case-study answer should demonstrate:

- product judgment
- architectural discipline
- private-equity operating context
- practical SDLC modernization
- agentic coding enablement
- governance and eval awareness
- a path from diagnostic insight to repeatable automation

The product should argue that the right first move in a PE setting is not to impose a factory, but to build the profiler, adaptation layer, and operating model that make factory adoption repeatable across heterogeneous companies.
