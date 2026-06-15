# Recombined Agent Execution Waves Prompt

Use this prompt after the planning kickoff to recombine the original 20-agent manifest into practical implementation waves.

## Objective

Review the original 20-agent manifest and produce a smaller, safer, wave-based execution plan that preserves the intent of the original decomposition while reducing coordination risk, overlapping file ownership, and scope creep.

## Inputs

Use these inputs:

1. The planning-mode kickoff prompt.
2. The original 20-agent manifest supplied by the user.
3. The current repository structure.
4. Any existing conventions, package managers, tests, and documentation in the repository.

## Output Required

Produce a markdown plan with:

1. A short critique of the original 20-agent manifest.
2. A recombined wave plan.
3. The agents in each wave.
4. Each agent's purpose.
5. Owned files or directories for each agent.
6. Read-only dependencies for each agent.
7. Required outputs for each agent.
8. Tests or checks each agent should run.
9. Explicit non-goals for each agent.
10. Integration checkpoints between waves.
11. A recommended first agent task.

## Recommended Wave Structure

Use this wave structure unless the repository inspection reveals a better one.

### Wave 1: Foundation and Contracts

Purpose: establish product scope, architecture, shared contracts, and safety boundaries before feature work begins.

Candidate agents:

1. Product Decomposition Agent
2. Repository Architect Agent
3. Domain, Schema, Evidence, and Trace Agent
4. Policy and Safety Agent

Primary outputs:

- Architecture decision notes.
- Repository map.
- Shared schema contracts.
- Evidence and trace contracts.
- Policy contract.
- Initial acceptance criteria.

### Wave 2: Local Agent MVP

Purpose: prove developer-level adoption and first-safe-commit workflows through CLI-first local functionality.

Candidate agents:

1. Local CLI Shell Agent
2. Local Doctor and Repo Explanation Agent
3. First-Commit Guidance Agent
4. Agentic Coding Coach Agent
5. Harness and Eval Agent

Primary outputs:

- `sdlc-local doctor`
- `sdlc-local explain`
- `sdlc-local first-commit`
- `sdlc-local coach`
- `sdlc-local harness create`
- `sdlc-local eval patch-quality`
- Local reports and examples.

### Wave 3: Server Agent MVP

Purpose: prove portfolio-company SDLC inventory, classification, blueprint recommendation, and manifest compilation against fixtures.

Candidate agents:

1. Server CLI Shell Agent
2. Fixture Provider SDK Agent
3. Build Inventory and Classifier Agent
4. Blueprint Catalog Agent
5. Manifest Engine Agent

Primary outputs:

- `sdlc-server inventory --fixture synthetic-company`
- build-system classifier
- blueprint recommendation engine
- `DeliveryManifest` validator
- GitHub Actions compiler
- fixture-backed reports.

### Wave 4: Reporting, Demo, and Case Study Packaging

Purpose: integrate the vertical slice into a coherent demo and case-study narrative.

Candidate agents:

1. Reporting Agent
2. Demo Assembly Agent
3. Technical Lead Integration Agent
4. Case Study Packaging Agent

Primary outputs:

- Unified reports.
- Demo script.
- Integration fixes.
- Case-study narrative.
- Final validation checklist.

## Agent Coordination Rules

Each implementation agent must receive:

- owned files/directories,
- read-only dependencies,
- expected outputs,
- tests to run,
- integration contract,
- explicit non-goals.

Agents must not rewrite files outside their ownership unless the Technical Lead Integration Agent assigns it.

Later agents should integrate with prior outputs rather than replace them.

## Review Criteria

The recombined plan is successful if it:

- Preserves the product thesis.
- Produces a runnable vertical slice quickly.
- Keeps external integrations fixture-based for MVP.
- Minimizes overlapping edits.
- Makes evidence, policy, trace, evals, and reporting shared contracts.
- Leaves room for future live connectors without implementing them in MVP.
