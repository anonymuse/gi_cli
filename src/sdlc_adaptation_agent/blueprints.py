"""MVP blueprint catalog and recommendation engine."""

from __future__ import annotations

from typing import Any

from .inventory import inventory_fixture

BLUEPRINTS: dict[str, dict[str, Any]] = {
    "node-service-ci": {
        "name": "Node.js Service CI Blueprint",
        "languages": ["node"],
        "required_manifest_fields": ["runtime", "commands.install", "commands.build", "commands.test"],
    },
    "python-service-ci": {
        "name": "Python Service CI Blueprint",
        "languages": ["python"],
        "required_manifest_fields": ["runtime", "commands.install", "commands.build", "commands.test"],
    },
    "jvm-service-ci": {
        "name": "JVM Service CI Blueprint",
        "languages": ["java"],
        "required_manifest_fields": ["runtime", "commands.install", "commands.build", "commands.test"],
    },
    "legacy-assessment": {
        "name": "Legacy Repository Assessment Blueprint",
        "languages": ["unknown"],
        "required_manifest_fields": ["project", "evidence_outputs", "deployment.placeholder"],
    },
}


def recommend_blueprints(fixture_id: str) -> dict[str, Any]:
    inventory = inventory_fixture(fixture_id)
    recommendations: list[dict[str, Any]] = []

    for repo in inventory["repositories"]:
        blueprint_id = _blueprint_for(repo)
        blueprint = BLUEPRINTS[blueprint_id]
        caveats: list[str] = []
        if repo["confidence"] < 0.6:
            caveats.append("Low-confidence classification; perform human review before standardizing.")
        if not repo["test_command"]:
            caveats.append("No reliable test command inferred from fixture evidence.")

        recommendations.append(
            {
                "blueprint_id": blueprint_id,
                "blueprint_name": blueprint["name"],
                "target_repository_ids": [repo["repository_id"]],
                "rationale": _rationale(repo, blueprint["name"]),
                "required_manifest_fields": blueprint["required_manifest_fields"],
                "evidence_ids": repo["evidence_ids"],
                "confidence": repo["confidence"],
                "caveats": caveats,
            }
        )

    return {
        "fixture_id": fixture_id,
        "recommendations": recommendations,
        "catalog_size": len(BLUEPRINTS),
    }


def _blueprint_for(repo: dict[str, Any]) -> str:
    if repo["language"] == "node":
        return "node-service-ci"
    if repo["language"] == "python":
        return "python-service-ci"
    if repo["language"] == "java":
        return "jvm-service-ci"
    return "legacy-assessment"


def _rationale(repo: dict[str, Any], blueprint_name: str) -> str:
    if repo["language"] == "unknown":
        return f"Recommend {blueprint_name} because fixture evidence is too weak for CI standardization."
    return (
        f"Recommend {blueprint_name} because {repo['repository_name']} is classified as "
        f"{repo['language']} using {repo['build_system']} with confidence {repo['confidence']}."
    )
