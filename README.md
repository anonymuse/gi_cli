# Factory Fit Profiler

Factory Fit Profiler is a dual-mode SDLC adaptation agent for private-equity portfolio companies. Its mission is to determine how an SDLC factory should be applied to real, heterogeneous engineering organizations before standardization is imposed.

The project treats modernization as an operating capability, not a one-time tooling rollout. Portfolio companies often include legacy systems, uneven documentation, fragmented DevOps tooling, manual release processes, inherited architectures, vendor constraints, security requirements, and business obligations that cannot pause while a clean-room SDLC factory is introduced. Factory Fit Profiler creates the diagnostic, onboarding, governance, and automation layer that makes factory adoption repeatable across those conditions.

## Mission

Help operators and engineering teams move from portfolio-level SDLC ambiguity to evidence-backed factory adoption decisions.

Factory Fit Profiler does this by:

- Assessing repositories, delivery tooling, build systems, CI/CD patterns, artifact flows, scanners, and deployment conventions.
- Onboarding developers into safe agentic engineering practices from their local workstation.
- Retrofitting existing delivery paths into explicit, governed SDLC blueprints.
- Automating only after the current estate has been inventoried, classified, and mapped to an appropriate operating model.
- Governing recommendations with evidence, policy controls, traces, and repeatable evals.
- Scaling standardized delivery practices across portfolio companies without pretending every company is greenfield.

The core thesis is:

```text
Assess → Onboard → Retrofit → Automate → Govern → Scale
```

## Product Concept

Factory Fit Profiler has two coordinated execution modes that share common contracts, evidence records, policy controls, trace output, eval rubrics, blueprint recommendations, and reports.

### Local Workstation Agent

The local agent runs on a developer laptop under explicit user control. It is intended to help a developer understand a repository, adopt agentic coding practices safely, and make a first governed change.

Current and planned local responsibilities include:

- Inspect a local repository or fixture and produce structured findings.
- Explain repository purpose, build hints, and safe first-change suggestions.
- Generate a minimal local agent harness with policy gates and validation hooks.
- Evaluate patch quality using a repeatable rubric.
- Teach safe human-led AI coding, constrained autonomous coding, and agent harness creation.

### Server-Side SDLC Agent

The server-side agent is designed as a containerized service. In the MVP it operates against fixtures and synthetic portfolio-company data rather than live DevOps integrations.

Current and planned server responsibilities include:

- Inventory portfolio repositories and delivery tooling from fixture data.
- Classify build types, CI/CD conventions, scanner usage, artifact patterns, and deployment signals.
- Identify standardization opportunities.
- Recommend reusable SDLC blueprints with evidence.
- Validate a simplified `DeliveryManifest` abstraction.
- Compile a deterministic GitHub Actions workflow from a valid manifest.

## Why This Exists

A generic SDLC factory can fail when it standardizes before it understands. Private-equity portfolios rarely contain uniform engineering environments: each company may have different languages, build systems, release obligations, tooling maturity, team practices, and modernization constraints.

Factory Fit Profiler addresses that gap by becoming the adaptation layer between current-state reality and future-state SDLC factory adoption. It helps answer:

- What delivery patterns already exist?
- Which repositories are ready for standardization?
- Which teams need onboarding or remediation first?
- Which factory blueprints are appropriate for each application?
- What evidence supports each recommendation?
- What should be automated now, and what should remain governed or manual until readiness improves?

## MVP Scope

The current MVP is fixture-backed and intentionally narrow. It proves the end-to-end path from diagnostic insight to repeatable automation without connecting to production DevOps systems.

Implemented command surfaces include:

- `sdlc-server inventory --fixture synthetic-company` to classify synthetic portfolio repositories with evidence.
- `sdlc-server blueprints recommend --fixture synthetic-company` to recommend SDLC standardization blueprints.
- `sdlc-server manifest validate <path>` to validate MVP `DeliveryManifest` JSON.
- `sdlc-server manifest compile --target github-actions <path>` to compile a deterministic GitHub Actions workflow.

The intended first runnable demo also includes local-agent workflows for repository inspection, explanation, harness generation, and patch-quality evaluation.

## Non-Goals for the MVP

The MVP does not:

- Connect to live enterprise DevOps systems.
- Mutate remote DevOps platforms.
- Push code to remotes.
- Open production pull requests.
- Install system dependencies automatically.
- Support every language, framework, or CI provider.
- Perform live deployment orchestration.
- Provide unrestricted desktop automation.
- Read secrets, credential stores, SSH configuration, private keys, or private environment files.

## Domain Contracts

The project is organized around shared contracts that allow local and server workflows to produce comparable, governable output.

Key contracts include:

- `DeliveryManifest`: a simplified representation of project identity, runtime, install/build/test commands, optional scan command, package metadata, and evidence outputs.
- Evidence records: citations for classifications, recommendations, eval findings, and report claims.
- Policy controls: rules for allowed, approval-gated, and forbidden actions.
- Trace records: execution and decision history for auditability.
- Eval records: repeatable scoring of patch quality and agent output.

## Repository Layout

```text
contracts/                    Shared JSON schemas for manifests, evidence, policy, trace, and evals
fixtures/synthetic-company/    Synthetic portfolio-company data and example manifests
src/sdlc_adaptation_agent/     Local and server CLI implementation modules
tests/                         Smoke and vertical-slice tests
docs/                          Planning, architecture, and execution notes
```


## Static Company Profile Demo

A static GitHub Pages demo is available under `docs/webapp/`. It accepts mocked company-profile markdown from a pasted textarea, uploaded `.md` file, or bundled sample and turns it into a browser-only readiness profile.

The demo is designed to illustrate the README thesis without requiring backend services or live DevOps integrations:

- Parse repository sections from markdown input.
- Classify language, build system, CI/CD hints, and evidence signals.
- Summarize factory readiness across the company.
- Recommend the same style of SDLC blueprint lanes used by the fixture-backed CLI.

To run locally, serve the repository root with any static file server and open `docs/webapp/index.html`:

```bash
python -m http.server 8000
```

Then visit `http://localhost:8000/docs/webapp/`. For GitHub Pages, configure Pages to publish from the repository `docs/` folder and use `/webapp/` as the demo path.

## Example Commands

Run the fixture-backed server vertical slice:

```bash
PYTHONPATH=src python -m sdlc_adaptation_agent.server_cli inventory --fixture synthetic-company
PYTHONPATH=src python -m sdlc_adaptation_agent.server_cli blueprints recommend --fixture synthetic-company
PYTHONPATH=src python -m sdlc_adaptation_agent.server_cli manifest validate fixtures/synthetic-company/delivery-manifest.valid.json
PYTHONPATH=src python -m sdlc_adaptation_agent.server_cli manifest compile --target github-actions fixtures/synthetic-company/delivery-manifest.valid.json
```

Run the test suite:

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```

## Development Principles

- Prefer evidence-backed recommendations over undocumented assertions.
- Prefer incremental adaptation over wholesale replacement.
- Keep the MVP fixture-backed until the domain model and governance contracts are stable.
- Treat local developer assistance and server-side portfolio analysis as two modes of the same operating model.
- Make every recommendation traceable, policy-aware, and evaluable.
- Optimize for practical PE operating leverage: readiness assessment, repeatable onboarding, governed automation, and scalable factory adoption.
