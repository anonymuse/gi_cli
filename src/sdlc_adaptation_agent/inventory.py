"""Fixture-backed inventory and build classification."""

from __future__ import annotations

from typing import Any

from .fixtures import load_company_fixture


def _evidence(repo_id: str, path: str, observed: str, confidence: float) -> dict[str, Any]:
    return {
        "id": f"ev-{repo_id}-{path.replace('/', '-').replace('.', '-')}",
        "source_type": "fixture",
        "source_location": f"fixtures/synthetic-company/{repo_id}/{path}",
        "observed_value": observed,
        "timestamp": "2026-06-15T00:00:00Z",
        "confidence": confidence,
        "related_finding_id": f"finding-{repo_id}",
    }


def classify_repository(repository: dict[str, Any]) -> dict[str, Any]:
    repo_id = repository["id"]
    files: dict[str, str] = repository.get("files", {})
    file_names = set(files)
    evidence: list[dict[str, Any]] = []

    result: dict[str, Any] = {
        "repository_id": repo_id,
        "repository_name": repository["name"],
        "language": "unknown",
        "runtime_version": "unknown",
        "package_manager": "unknown",
        "build_system": "unknown",
        "install_command": None,
        "build_command": None,
        "test_command": None,
        "scan_command": None,
        "ci_cd_hints": [],
        "confidence": 0.35,
        "evidence_ids": [],
    }

    if "package.json" in file_names:
        evidence.append(_evidence(repo_id, "package.json", "Node package manifest with build/test scripts", 0.9))
        result.update(
            language="node",
            runtime_version="20",
            package_manager="npm" if "package-lock.json" in file_names else "node-package-manager",
            build_system="npm-scripts",
            install_command="npm ci" if "package-lock.json" in file_names else "npm install",
            build_command="npm run build",
            test_command="npm test",
            scan_command="npm audit --audit-level=high",
            confidence=0.9,
        )
    elif "pyproject.toml" in file_names:
        evidence.append(_evidence(repo_id, "pyproject.toml", "Python project metadata with pytest hints", 0.88))
        result.update(
            language="python",
            runtime_version="3.11",
            package_manager="poetry" if "poetry.lock" in file_names else "pip",
            build_system="pyproject",
            install_command="poetry install" if "poetry.lock" in file_names else "python -m pip install -e .",
            build_command="python -m build",
            test_command="python -m pytest",
            scan_command="python -m pip audit",
            confidence=0.88,
        )
    elif "pom.xml" in file_names:
        evidence.append(_evidence(repo_id, "pom.xml", "Maven project descriptor", 0.87))
        result.update(
            language="java",
            runtime_version="17",
            package_manager="maven",
            build_system="maven",
            install_command="mvn dependency:go-offline",
            build_command="mvn package",
            test_command="mvn test",
            scan_command="mvn -q org.owasp:dependency-check-maven:check",
            confidence=0.87,
        )
    elif "build.sh" in file_names:
        evidence.append(_evidence(repo_id, "build.sh", "Legacy shell build script without structured metadata", 0.45))
        result.update(
            build_system="legacy-shell-script",
            build_command="./build.sh",
            confidence=0.45,
        )

    for ci_path in [".github/workflows/ci.yml", ".github/workflows/python.yml", "Jenkinsfile"]:
        if ci_path in file_names:
            evidence.append(_evidence(repo_id, ci_path, "CI/CD configuration hint", 0.8))
            result["ci_cd_hints"].append(ci_path)

    result["evidence"] = evidence
    result["evidence_ids"] = [item["id"] for item in evidence]
    return result


def inventory_fixture(fixture_id: str) -> dict[str, Any]:
    company = load_company_fixture(fixture_id)
    repositories = [classify_repository(repo) for repo in company.repositories]
    return {
        "fixture_id": company.id,
        "company_name": company.name,
        "repositories": repositories,
        "summary": {
            "repository_count": len(repositories),
            "classified_count": sum(1 for repo in repositories if repo["language"] != "unknown"),
            "low_confidence_count": sum(1 for repo in repositories if repo["confidence"] < 0.6),
        },
    }
