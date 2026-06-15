"""Smoke and vertical-slice tests for the CLI command surfaces."""

from __future__ import annotations

import io
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from sdlc_adaptation_agent import local_cli, server_cli, windows_guide
from sdlc_adaptation_agent.blueprints import recommend_blueprints
from sdlc_adaptation_agent.fixtures import load_company_fixture
from sdlc_adaptation_agent.inventory import inventory_fixture
from sdlc_adaptation_agent.manifest import compile_manifest_file, validate_manifest_file

FIXTURE_ROOT = Path("fixtures/synthetic-company")
VALID_MANIFEST = FIXTURE_ROOT / "delivery-manifest.valid.json"
INVALID_MANIFEST = FIXTURE_ROOT / "delivery-manifest.invalid.json"


class LocalCliSmokeTests(unittest.TestCase):
    def test_local_commands_are_discoverable(self) -> None:
        parser = local_cli.build_parser()
        help_text = parser.format_help()

        for command in ["doctor", "explain", "first-commit", "coach", "windows-guide", "harness", "eval"]:
            with self.subTest(command=command):
                self.assertIn(command, help_text)

    def test_nested_local_commands_run_as_placeholders(self) -> None:
        self.assertEqual(local_cli.main(["harness", "create"]), 0)
        self.assertEqual(local_cli.main(["eval", "patch-quality"]), 0)

    def test_windows_guide_summary_covers_required_workflow(self) -> None:
        output = io.StringIO()
        with redirect_stdout(output):
            exit_code = local_cli.main(["windows-guide", "--summary"])

        summary = output.getvalue()
        self.assertEqual(exit_code, 0)
        self.assertIn("GitHub", summary)
        self.assertIn("Claude CLI", summary)
        self.assertIn("Visual Studio", summary)
        self.assertIn("GenAI", summary)
        self.assertIn("human", summary.lower())
        self.assertIn("merge", summary.lower())

    def test_windows_guide_steps_are_human_gated(self) -> None:
        self.assertGreaterEqual(len(windows_guide.WORKFLOW_STEPS), 6)
        for step in windows_guide.WORKFLOW_STEPS:
            with self.subTest(step=step.title):
                self.assertTrue(step.human_action)
                self.assertTrue(step.genai_action)
                self.assertTrue(step.automation)


class ServerCliSmokeTests(unittest.TestCase):
    def test_server_commands_are_discoverable(self) -> None:
        parser = server_cli.build_parser()
        help_text = parser.format_help()

        for command in ["inventory", "blueprints", "manifest"]:
            with self.subTest(command=command):
                self.assertIn(command, help_text)

    def test_server_inventory_command_runs(self) -> None:
        self.assertEqual(server_cli.main(["inventory", "--fixture", "synthetic-company"]), 0)

    def test_server_blueprints_command_runs(self) -> None:
        self.assertEqual(server_cli.main(["blueprints", "recommend", "--fixture", "synthetic-company"]), 0)

    def test_server_manifest_commands_run(self) -> None:
        self.assertEqual(server_cli.main(["manifest", "validate", str(VALID_MANIFEST)]), 0)
        self.assertEqual(server_cli.main(["manifest", "validate", str(INVALID_MANIFEST)]), 1)
        self.assertEqual(
            server_cli.main(["manifest", "compile", "--target", "github-actions", str(VALID_MANIFEST)]),
            0,
        )


class ServerWaveThreeTests(unittest.TestCase):
    def test_fixture_loader_loads_synthetic_company(self) -> None:
        fixture = load_company_fixture("synthetic-company")

        self.assertEqual(fixture.id, "synthetic-company")
        self.assertEqual(len(fixture.repositories), 4)
        self.assertEqual({repo["id"] for repo in fixture.repositories}, {
            "repo-node-web",
            "repo-python-api",
            "repo-java-batch",
            "repo-legacy-tools",
        })

    def test_inventory_classifies_all_fixture_repositories_with_evidence(self) -> None:
        inventory = inventory_fixture("synthetic-company")

        self.assertEqual(inventory["summary"]["repository_count"], 4)
        self.assertEqual(inventory["summary"]["classified_count"], 3)
        self.assertEqual(inventory["summary"]["low_confidence_count"], 1)
        for repository in inventory["repositories"]:
            with self.subTest(repository=repository["repository_id"]):
                self.assertGreater(repository["confidence"], 0)
                self.assertTrue(repository["evidence_ids"])
                self.assertTrue(repository["evidence"])

    def test_blueprint_recommendations_cover_fixture_repositories(self) -> None:
        recommendations = recommend_blueprints("synthetic-company")["recommendations"]

        self.assertEqual(len(recommendations), 4)
        blueprint_ids = {item["blueprint_id"] for item in recommendations}
        self.assertIn("node-service-ci", blueprint_ids)
        self.assertIn("python-service-ci", blueprint_ids)
        self.assertIn("jvm-service-ci", blueprint_ids)
        self.assertIn("legacy-assessment", blueprint_ids)
        for recommendation in recommendations:
            with self.subTest(recommendation=recommendation["blueprint_id"]):
                self.assertTrue(recommendation["evidence_ids"])
                self.assertTrue(recommendation["required_manifest_fields"])

    def test_manifest_validation_accepts_valid_and_rejects_invalid(self) -> None:
        self.assertTrue(validate_manifest_file(VALID_MANIFEST)["valid"])
        invalid_result = validate_manifest_file(INVALID_MANIFEST)
        self.assertFalse(invalid_result["valid"])
        self.assertIn("project.name is required", invalid_result["errors"])
        self.assertIn("deployment.placeholder must be true for the MVP", invalid_result["errors"])

    def test_github_actions_compiler_is_deterministic(self) -> None:
        first = compile_manifest_file(VALID_MANIFEST, "github-actions")
        second = compile_manifest_file(VALID_MANIFEST, "github-actions")

        self.assertEqual(first, second)
        self.assertIn("uses: actions/setup-node@v4", first)
        self.assertIn("run: npm ci", first)
        self.assertIn("run: npm run build", first)
        self.assertIn("run: npm test", first)
        self.assertIn("run: npm audit --audit-level=high", first)
        self.assertIn("Deployment is intentionally out of MVP scope", first)

    def test_compile_command_prints_workflow(self) -> None:
        output = io.StringIO()
        with redirect_stdout(output):
            exit_code = server_cli.main(["manifest", "compile", "--target", "github-actions", str(VALID_MANIFEST)])

        self.assertEqual(exit_code, 0)
        self.assertIn("name: delivery-manifest-ci", output.getvalue())


if __name__ == "__main__":
    unittest.main()
