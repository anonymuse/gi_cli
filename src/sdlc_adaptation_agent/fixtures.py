"""Fixture loading utilities for server-side MVP workflows."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
FIXTURES_ROOT = REPO_ROOT / "fixtures"


@dataclass(frozen=True)
class SyntheticCompany:
    """Loaded synthetic portfolio-company fixture."""

    id: str
    name: str
    repositories: list[dict[str, Any]]


def fixture_path(fixture_id: str) -> Path:
    return FIXTURES_ROOT / fixture_id


def load_company_fixture(fixture_id: str) -> SyntheticCompany:
    path = fixture_path(fixture_id) / "company.json"
    if not path.exists():
        raise ValueError(f"Unknown fixture '{fixture_id}'. Expected {path} to exist.")
    payload = json.loads(path.read_text(encoding="utf-8"))
    return SyntheticCompany(
        id=payload["id"],
        name=payload["name"],
        repositories=list(payload.get("repositories", [])),
    )
