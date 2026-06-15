# Wave 2 Execution Prompt: Local Agent MVP

Use this prompt after Wave 1 has established the foundation contracts, repository map, architecture notes, schemas, policy contract, evidence and trace model, initial acceptance criteria, and implementation ownership boundaries.

## Role

You are the Wave 2 implementation lead for the Dual-Mode SDLC Adaptation Agent.

Your job is to execute the **Local Agent MVP** as a narrow, CLI-first vertical slice that proves developer-level adoption and first-safe-commit workflows without expanding into server-side inventory, live enterprise integrations, unrestricted automation, or broad platform work.

## Objective

Implement the local workstation MVP commands and supporting local reports using the contracts produced in Wave 1.

Wave 2 should prove that a developer can:

1. Inspect a local repository safely.
2. Understand repository purpose and build/test hints.
3. Receive first-safe-commit guidance.
4. Get coaching for human-led agentic coding practices.
5. Create a minimal local agent harness with policy gates and validation hooks.
6. Evaluate patch quality using a repeatable, evidence-backed rubric.

## Required Context Before Starting

First inspect the current repository state and Wave 1 outputs. Do not assume exact file names if the repository has evolved.

Use these inputs:

1. `docs/prompts/planning-mode-kickoff.md`
2. `docs/prompts/original-manifest-review.md`
3. `docs/prompts/agent-execution-waves.md`
4. All Wave 1 architecture, schema, policy, evidence, trace, and acceptance-criteria outputs.
5. Existing package manager, test framework, CLI conventions, and documentation in the repository.

If a required Wave 1 contract is missing, create only the smallest local placeholder needed to unblock Wave 2 and document it as a follow-up for Wave 1 alignment. Do not redesign the foundation during Wave 2.

## Scope

Implement the Wave 2 Local Agent MVP commands:

1. `sdlc-local doctor`
2. `sdlc-local explain`
3. `sdlc-local first-commit`
4. `sdlc-local coach`
5. `sdlc-local harness create`
6. `sdlc-local eval patch-quality`

Also implement the minimum shared local report examples, fixtures, and tests needed to demonstrate these commands end-to-end.

## Non-Goals

Wave 2 must not:

- Implement server-side portfolio inventory.
- Implement blueprint recommendation beyond local read-only hints.
- Implement `DeliveryManifest` compilation.
- Connect to live DevOps, SCM, ticketing, artifact, CI/CD, scanner, or cloud APIs.
- Push commits, open pull requests, or mutate remote systems.
- Install system dependencies automatically.
- Read secrets, credential stores, SSH config, private key files, or `.env` files.
- Perform unrestricted desktop automation.
- Rewrite Wave 1 contracts unless explicitly required to fix a blocking inconsistency.
- Add broad framework support beyond what is needed for the fixture-backed MVP.

## Agent Assignments

Use the following agents. Keep file ownership disjoint. Agents may read shared contracts and prior outputs but should not rewrite files outside their ownership.

### 1. Local CLI Shell Agent

**Purpose:** Create the local CLI command surface and routing for all Wave 2 commands.

**Owns:**

- Local CLI entrypoint files.
- Command parser or router files for `sdlc-local`.
- CLI help text and command-level documentation stubs.

**Reads:**

- Wave 1 architecture notes.
- Shared schema, policy, evidence, trace, and eval contracts.
- Existing CLI conventions and package configuration.

**Produces:**

- Runnable `sdlc-local` CLI shell.
- Placeholder command handlers for all Wave 2 commands.
- Help output showing arguments, options, and safe default behavior.

**Tests/checks:**

- CLI help command succeeds.
- Each Wave 2 command is discoverable.
- Unknown commands produce actionable errors.

**Non-goals:**

- Implement full doctor, explanation, harness, or eval business logic.
- Add server-side commands.

### 2. Local Doctor and Repo Explanation Agent

**Purpose:** Implement safe repository inspection and evidence-backed explanations.

**Owns:**

- Local repository inspection module.
- `sdlc-local doctor` handler.
- `sdlc-local explain` handler.
- Local report serializers for doctor and explain outputs.
- Tests and fixtures specific to doctor/explain behavior.

**Reads:**

- CLI shell files.
- Evidence and trace contracts.
- Policy contract.
- Repository map and architecture notes.

**Produces:**

- `sdlc-local doctor` report with structured findings and evidence IDs.
- `sdlc-local explain` summary with repository purpose, build hints, test hints, safe first-change suggestions, and cited evidence.
- Fixture-backed examples for at least one simple repository.

**Tests/checks:**

- Doctor command works against a fixture repository.
- Explain command works against the same fixture repository.
- Output includes evidence references for claims.
- Secret-like files are skipped according to policy.

**Non-goals:**

- Deep language-specific static analysis.
- Live package vulnerability scanning.
- Modifying inspected repositories.

### 3. First-Commit Guidance Agent

**Purpose:** Guide a developer toward a safe first commit using findings from doctor and explain.

**Owns:**

- `sdlc-local first-commit` handler.
- First-commit guidance templates.
- Tests and fixtures for safe-change recommendations.

**Reads:**

- Doctor/explain report shapes.
- Policy contract.
- Evidence model.
- CLI shell files.

**Produces:**

- A first-commit guidance report that recommends low-risk changes.
- Explicit safety checklist before editing.
- Suggested validation commands based on repository evidence.

**Tests/checks:**

- First-commit guidance can consume fixture doctor/explain data.
- Guidance avoids unsafe files and secret-like paths.
- Guidance includes validation steps and evidence citations.

**Non-goals:**

- Automatically editing files.
- Creating commits.
- Running package managers without explicit user action.

### 4. Agentic Coding Coach Agent

**Purpose:** Provide concise, actionable coaching for human-led AI coding, constrained autonomous coding, and local harness usage.

**Owns:**

- `sdlc-local coach` handler.
- Coaching content templates.
- Tests for deterministic coaching output.

**Reads:**

- Policy contract.
- Eval contract.
- Harness contract.
- CLI shell files.

**Produces:**

- Coaching output for local agentic coding modes.
- Safety reminders tied to the local action policy.
- Suggested next command sequence for a new developer.

**Tests/checks:**

- Coach command renders deterministic guidance.
- Guidance references policy boundaries.
- Guidance recommends Wave 2 commands in a coherent order.

**Non-goals:**

- Interactive tutoring UI.
- Background agents.
- Autonomous desktop control.

### 5. Harness and Eval Agent

**Purpose:** Implement local harness scaffolding and patch-quality evaluation.

**Owns:**

- `sdlc-local harness create` handler.
- Harness template files.
- `sdlc-local eval patch-quality` handler.
- Patch-quality rubric implementation.
- Harness and eval tests/fixtures.

**Reads:**

- Policy contract.
- Evidence, trace, and eval contracts.
- CLI shell files.
- Doctor/explain outputs where useful.

**Produces:**

- A minimal generated local agent harness with policy gates and validation hooks.
- A repeatable patch-quality evaluation report with scores for correctness, buildability, minimality, safety, explainability, evidence use, and policy compliance.
- Fixture sample patch inputs and expected eval output.

**Tests/checks:**

- Harness creation writes only to the requested output directory.
- Generated harness includes policy gates and validation hooks.
- Patch-quality eval produces deterministic scores and overall status.
- Eval output conforms to the Wave 1 eval contract.

**Non-goals:**

- Running untrusted generated code automatically.
- Full benchmark infrastructure.
- LLM-as-judge integration unless already established by Wave 1 and fixture-backed.

## Implementation Rules

1. Prefer the smallest vertical slice that can be tested end-to-end.
2. Reuse Wave 1 contracts instead of inventing parallel schemas.
3. Keep command outputs deterministic where practical.
4. Every claim in reports should cite an evidence record.
5. Default to read-only repository inspection.
6. Skip secret-like files and sensitive paths.
7. Keep external integrations fixture-backed.
8. Avoid overlapping file ownership between agents.
9. Document any contract gaps as follow-ups instead of expanding scope.
10. Update README or prompt documentation only where necessary to make Wave 2 runnable.

## Expected Final Deliverables

At the end of Wave 2, provide:

1. A summary of implemented commands.
2. A command-by-command ownership report.
3. Example outputs or paths to generated reports.
4. Tests/checks run and their results.
5. Known limitations and follow-ups for Wave 3.
6. Confirmation that no live enterprise integrations or remote mutations were added.

## Integration Checkpoint Before Wave 3

Wave 2 is complete only when:

1. `sdlc-local --help` or equivalent help output lists the Wave 2 commands.
2. `sdlc-local doctor` works against a fixture or local repository.
3. `sdlc-local explain` produces evidence-backed repository guidance.
4. `sdlc-local first-commit` produces safe, non-mutating first-change guidance.
5. `sdlc-local coach` explains the recommended local workflow and policy boundaries.
6. `sdlc-local harness create` creates a minimal harness in a caller-specified output directory.
7. `sdlc-local eval patch-quality` evaluates a sample patch with the agreed rubric.
8. Tests cover the core behavior of each command.
9. Documentation explains how to run the local MVP demo.
10. Any deviations from Wave 1 contracts are recorded as explicit follow-ups.

## Recommended First Task

Start with the Local CLI Shell Agent.

Create the `sdlc-local` command shell with discoverable placeholders for all Wave 2 commands, then add one fixture-backed happy-path test for command discovery. This gives the other Wave 2 agents stable integration points without forcing them to coordinate on CLI routing details.
