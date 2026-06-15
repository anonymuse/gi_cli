# Original 20-Agent Manifest Review Prompt

Use this prompt when the original 20-agent manifest is available and needs to be reviewed before implementation.

## Role

You are the technical lead reviewing a proposed multi-agent implementation manifest for the Dual-Mode SDLC Adaptation Agent.

Your job is to preserve the useful decomposition while recombining overlapping work into safer implementation waves.

## Review Instructions

Review the original manifest for:

1. Overlapping ownership.
2. Missing shared contracts.
3. Agents likely to overbuild.
4. Agents likely to block other agents.
5. Agents that should be merged.
6. Agents that should be split.
7. Agents that should be delayed until after the first vertical slice.
8. Missing validation steps.
9. Missing fixture/demo requirements.
10. Missing policy, evidence, trace, or eval requirements.

## Required Output Format

Produce the following sections:

### 1. Manifest Summary

Briefly summarize the original 20-agent manifest and its intent.

### 2. Strengths

List the parts of the manifest that should be preserved.

### 3. Risks

List coordination, scope, architecture, and integration risks.

### 4. Recombination Recommendations

For each original agent, classify it as one of:

- keep as-is
- merge
- split
- delay
- remove from MVP

Provide a short reason for each classification.

### 5. Proposed Wave Plan

Recombine the manifest into these waves:

1. Foundation and Contracts
2. Local Agent MVP
3. Server Agent MVP
4. Reporting, Demo, and Case Study Packaging

### 6. Ownership Matrix

Create a table with:

| Wave | Agent | Owns | Reads | Produces | Tests/Checks | Non-Goals |
| --- | --- | --- | --- | --- | --- | --- |

### 7. Integration Checkpoints

Define the checkpoint required at the end of each wave before the next wave starts.

### 8. First Implementation Task

Recommend the first implementation task after planning mode completes.

The first task should be small, low-risk, and should establish contracts or CLI skeletons needed by later work.

## Constraints

- Do not start coding.
- Do not expand the MVP beyond the thin slice.
- Do not introduce live enterprise API integration in MVP.
- Do not create overlapping write ownership between agents.
- Prefer fixture-backed demos over live systems.
- Prefer explicit contracts over implicit coupling.
