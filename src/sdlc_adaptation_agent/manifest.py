"""DeliveryManifest validation and GitHub Actions compilation."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

SUPPORTED_TARGET = "github-actions"


class ManifestError(ValueError):
    """Raised when a DeliveryManifest is invalid."""


def load_manifest(path: str | Path) -> dict[str, Any]:
    manifest_path = Path(path)
    if not manifest_path.exists():
        raise ManifestError(f"Manifest file not found: {manifest_path}")
    try:
        return json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ManifestError(f"Manifest is not valid JSON: {exc}") from exc


def validate_manifest_payload(manifest: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    _require_string(manifest, ["id"], errors)
    _require_string(manifest, ["project", "name"], errors)
    _require_string(manifest, ["project", "repository_id"], errors)
    _require_string(manifest, ["runtime", "language"], errors)
    _require_string(manifest, ["runtime", "version"], errors)
    _require_string(manifest, ["commands", "install"], errors)
    _require_string(manifest, ["commands", "build"], errors)
    _require_string(manifest, ["commands", "test"], errors)

    deployment = manifest.get("deployment")
    if not isinstance(deployment, dict) or deployment.get("placeholder") is not True:
        errors.append("deployment.placeholder must be true for the MVP")

    evidence_outputs = manifest.get("evidence_outputs")
    if not isinstance(evidence_outputs, list) or not all(isinstance(item, str) for item in evidence_outputs):
        errors.append("evidence_outputs must be a list of evidence id strings")

    return errors


def validate_manifest_file(path: str | Path) -> dict[str, Any]:
    manifest = load_manifest(path)
    errors = validate_manifest_payload(manifest)
    return {
        "valid": not errors,
        "errors": errors,
        "manifest_id": manifest.get("id"),
    }


def compile_manifest_file(path: str | Path, target: str) -> str:
    if target != SUPPORTED_TARGET:
        raise ManifestError(f"Unsupported target '{target}'. Supported target: {SUPPORTED_TARGET}")
    manifest = load_manifest(path)
    errors = validate_manifest_payload(manifest)
    if errors:
        raise ManifestError("Cannot compile invalid DeliveryManifest: " + "; ".join(errors))
    return compile_github_actions(manifest)


def compile_github_actions(manifest: dict[str, Any]) -> str:
    commands = manifest["commands"]
    runtime = manifest["runtime"]
    setup_action = _setup_action(runtime["language"])
    lines = [
        "name: delivery-manifest-ci",
        "on:",
        "  pull_request:",
        "  push:",
        "    branches: [ main ]",
        "jobs:",
        "  build-test:",
        "    runs-on: ubuntu-latest",
        "    steps:",
        "      - uses: actions/checkout@v4",
        f"      - name: Set up {runtime['language']} {runtime['version']}",
        f"        uses: {setup_action}",
        "        with:",
        f"          {_version_key(runtime['language'])}: '{runtime['version']}'",
        "      - name: Install",
        f"        run: {commands['install']}",
        "      - name: Build",
        f"        run: {commands['build']}",
        "      - name: Test",
        f"        run: {commands['test']}",
    ]
    if commands.get("scan"):
        lines.extend(["      - name: Scan", f"        run: {commands['scan']}"])
    lines.extend([
        "      - name: Deployment placeholder",
        "        run: echo 'Deployment is intentionally out of MVP scope.'",
    ])
    return "\n".join(lines) + "\n"


def _require_string(payload: dict[str, Any], path: list[str], errors: list[str]) -> None:
    current: Any = payload
    for segment in path:
        if not isinstance(current, dict) or segment not in current:
            errors.append(f"{'.'.join(path)} is required")
            return
        current = current[segment]
    if not isinstance(current, str) or not current.strip():
        errors.append(f"{'.'.join(path)} must be a non-empty string")


def _setup_action(language: str) -> str:
    if language == "node":
        return "actions/setup-node@v4"
    if language == "python":
        return "actions/setup-python@v5"
    if language == "java":
        return "actions/setup-java@v4"
    return "actions/setup-node@v4"


def _version_key(language: str) -> str:
    if language == "node":
        return "node-version"
    if language == "python":
        return "python-version"
    if language == "java":
        return "java-version"
    return "node-version"
