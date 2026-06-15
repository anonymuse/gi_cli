# Wave 4 Execution Prompt: Reporting, Demo, and Case Study Packaging

Use this prompt after Waves 1 through 3 have produced a runnable, fixture-backed vertical slice.

## Objective

Execute Wave 4 from the agent execution waves plan: integrate reporting, demo assembly, technical-lead validation, and case-study packaging into one coherent MVP presentation without expanding scope beyond the fixture-backed CLI vertical slice.

Wave 4 should make the product easy to understand, run, validate, and explain to stakeholders.

## Required Inputs

Before starting, review:

1. `docs/prompts/agent-execution-waves.md`.
2. The final implementation outputs from Waves 1, 2, and 3.
3. Existing CLI commands, fixtures, generated reports, examples, tests, and documentation.
4. Any architecture, schema, evidence, trace, policy, or eval contracts created in earlier waves.
5. Current repository conventions for formatting, tests, package management, and documentation.

If any expected Wave 1-3 output is missing, document the gap and use the smallest fixture-backed fallback needed to complete the demo narrative. Do not introduce live external integrations.

## Wave 4 Scope

### Primary Outcome

Produce a polished, runnable case-study package that demonstrates the MVP end-to-end:

1. Local developer workflow.
2. Server-side portfolio inventory and manifest workflow.
3. Evidence, trace, policy, and evaluation outputs.
4. Unified reporting.
5. A concise demo script.
6. A final validation checklist.
7. A case-study narrative that explains the product thesis, constraints, implementation, and next steps.

### Non-Goals

Wave 4 must not:

- Add live third-party service integrations.
- Replace fixture-backed MVP behavior with network-dependent behavior.
- Redesign foundational schemas, contracts, or architecture unless required to fix integration defects.
- Expand the product beyond the original Dual-Mode SDLC Adaptation Agent thesis.
- Rewrite unrelated commands, tests, or documentation.
- Hide failing checks; document limitations clearly.

## Agent Assignments

Use four agents. Keep file ownership boundaries explicit. Agents may read other areas but must not edit outside their ownership unless the Technical Lead Integration Agent assigns the change.

### Agent 1: Reporting Agent

**Purpose:** Create or refine unified reporting that ties together local CLI outputs, server inventory outputs, manifest outputs, evidence, trace, policy, and eval results.

**Owned files/directories:**

- Report-generation modules and templates.
- Report fixtures and expected report snapshots.
- Documentation specifically describing report fields or report formats.

**Read-only dependencies:**

- CLI command implementations from Waves 2 and 3.
- Shared schemas and validators.
- Fixture data.
- Evidence, trace, policy, and eval contracts.

**Required outputs:**

- A unified report format for the MVP demo.
- Example generated reports for the synthetic fixture scenario.
- Clear report-field documentation.
- Tests or snapshot checks for report generation.

**Tests/checks to run:**

- Report unit tests.
- Snapshot or golden-file checks, if the repository uses them.
- Any CLI command that generates the unified report from fixtures.

**Non-goals:**

- Do not change domain contracts except to fix integration defects approved by the Technical Lead Integration Agent.
- Do not add dashboard UI work unless it already exists and only needs documentation or fixture wiring.

### Agent 2: Demo Assembly Agent

**Purpose:** Package the vertical slice into a repeatable demo flow that a reviewer can run locally.

**Owned files/directories:**

- Demo scripts.
- Demo fixture orchestration files.
- README sections or docs dedicated to running the demo.
- Example command transcripts, if maintained in the repository.

**Read-only dependencies:**

- Local CLI commands from Wave 2.
- Server CLI commands from Wave 3.
- Unified reporting outputs from Agent 1.
- Existing fixtures and generated examples.

**Required outputs:**

- A step-by-step demo script.
- Copy-pasteable commands for the full happy path.
- Expected outputs or output excerpts for each step.
- Troubleshooting notes for common local setup problems.

**Tests/checks to run:**

- Execute the documented demo commands against fixtures.
- Run repository formatting or lint checks for touched docs/scripts.
- Verify generated artifacts land in documented locations.

**Non-goals:**

- Do not introduce new product behavior solely for the demo.
- Do not make the demo depend on secrets, network access, or live provider credentials.

### Agent 3: Technical Lead Integration Agent

**Purpose:** Own cross-agent integration, resolve small compatibility defects, and confirm the end-to-end MVP is coherent.

**Owned files/directories:**

- Integration glue files needed to connect prior wave outputs.
- Minimal contract adapters required for report/demo consistency.
- Final validation checklist.
- Release-readiness or integration notes.

**Read-only dependencies:**

- All Wave 1-4 outputs.
- Tests, fixtures, schemas, and docs across the repository.

**Required outputs:**

- A final validation checklist.
- A list of integration fixes made, with rationale.
- Confirmation that local and server workflows can run in a single fixture-backed sequence.
- A concise inventory of any remaining known gaps.

**Tests/checks to run:**

- Full relevant test suite, or the narrowest documented equivalent if the full suite is not available.
- End-to-end fixture command sequence.
- Lint/typecheck/format commands used by the repository.

**Non-goals:**

- Do not refactor unrelated internals.
- Do not override agent ownership boundaries except for explicitly documented integration fixes.
- Do not defer obvious broken demo-path defects without documenting why.

### Agent 4: Case Study Packaging Agent

**Purpose:** Turn the completed MVP into a case-study narrative suitable for portfolio-company, technical, or investor review.

**Owned files/directories:**

- Case-study markdown files.
- Narrative README sections.
- Architecture/demo summary diagrams or text-only equivalents.
- Final packaging docs.

**Read-only dependencies:**

- Product thesis and scope from Wave 1.
- Demo script from Agent 2.
- Unified report examples from Agent 1.
- Final validation checklist from Agent 3.

**Required outputs:**

- A case-study narrative covering problem, users, MVP scope, architecture, workflow, evidence model, demo path, validation results, limitations, and next steps.
- A short executive summary.
- A technical appendix or links to implementation docs.
- Clear statements of what is fixture-backed versus future live integration work.

**Tests/checks to run:**

- Markdown lint or formatting checks, if available.
- Link checks, if available.
- Manual consistency pass against the demo commands and validation checklist.

**Non-goals:**

- Do not exaggerate implemented capabilities.
- Do not imply live integrations exist if the MVP is fixture-backed.
- Do not duplicate large sections of implementation docs; link to them instead.

## Execution Order

1. Start Agent 1 and Agent 2 in parallel if reporting and demo ownership are independent enough.
2. Run Agent 3 after the first usable reporting and demo outputs exist.
3. Run Agent 4 after the demo flow and validation checklist are stable.
4. Finish with a final maintainer pass that verifies docs, commands, generated outputs, and known gaps are consistent.

## Integration Checkpoints

### Checkpoint A: Reporting Contract

Confirm:

- The unified report can be generated from fixture data.
- Report fields map to existing schemas or documented derived values.
- Evidence, trace, policy, and eval sections are present or explicitly marked unavailable.

### Checkpoint B: Demo Reproducibility

Confirm:

- A fresh reviewer can follow the documented commands.
- Commands do not require secrets or live network dependencies.
- Expected outputs match generated artifacts closely enough for review.

### Checkpoint C: End-to-End Validation

Confirm:

- Local and server workflows can be demonstrated in one narrative.
- Tests/checks for touched areas pass or limitations are documented.
- Any remaining gaps are listed with owner, impact, and recommended follow-up.

### Checkpoint D: Case Study Readiness

Confirm:

- The case study accurately reflects what was implemented.
- The narrative preserves the product thesis.
- Future work is clearly separated from completed MVP behavior.

## Final Output Required

Return a markdown summary with:

1. Files changed, grouped by agent.
2. Demo commands and where their outputs are written.
3. Tests/checks run, including pass/fail status.
4. Known gaps or limitations.
5. Recommended follow-up work.
6. The final validation checklist.

## Starter Task for the First Agent

Start with the Reporting Agent:

> Inspect the existing Wave 1-3 schemas, fixtures, CLI outputs, and eval artifacts. Design the smallest unified fixture-backed report that demonstrates the MVP end-to-end. Implement or document the report format, generate an example report from the synthetic fixture scenario, and add the narrowest useful tests or checks. Do not modify core schemas unless a Technical Lead Integration Agent approves the integration fix.
