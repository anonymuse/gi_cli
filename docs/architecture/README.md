# Architecture

Factory Fit Profiler uses the product specification as the architectural source of truth. The architecture is organized around a six-stage factory adoption lifecycle:

```text
Assess → Onboard → Retrofit → Automate → Govern → Scale
```

See the product specification for the canonical product diagram and lifecycle definitions: [`docs/product/factory-fit-profiler-product-spec.md`](../product/factory-fit-profiler-product-spec.md).

## Architecture Views

- [`wave-1.md`](wave-1.md): foundation and contract scope for the fixture-backed MVP.
- [`diagrams/factory-fit-profiler-architecture.mmd`](diagrams/factory-fit-profiler-architecture.mmd): Mermaid source for the canonical architecture diagram used by README-level documentation.

## Contract-Centered Design

The same contract families support local workstation and server-side workflows:

| Contract | Architectural role |
| --- | --- |
| `DeliveryManifest` | Normalizes application delivery intent before workflow compilation. |
| Evidence | Connects classifications, recommendations, and generated outputs to source facts. |
| Policy | Defines allowed, approval-gated, and forbidden actions. |
| Trace | Captures execution and decision history for auditability. |
| Eval | Scores patch quality and agent output using repeatable rubrics. |

## Mode Boundaries

- **Local Workstation Agent**: human-controlled repository inspection, explanation, harness generation, safe-first-change coaching, and patch-quality evaluation.
- **Server-Side SDLC Agent**: fixture-backed portfolio inventory, blueprint recommendation, manifest validation, and deterministic workflow compilation.

Both modes feed the governance layer. Neither MVP mode mutates remote systems or reads secrets.
