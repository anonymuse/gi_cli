"""Smoke tests for Wave 1 CLI command discovery."""

from __future__ import annotations

import unittest

from sdlc_adaptation_agent import local_cli, server_cli


class LocalCliSmokeTests(unittest.TestCase):
    def test_local_commands_are_discoverable(self) -> None:
        parser = local_cli.build_parser()
        help_text = parser.format_help()

        for command in ["doctor", "explain", "first-commit", "coach", "harness", "eval"]:
            with self.subTest(command=command):
                self.assertIn(command, help_text)

    def test_nested_local_commands_run_as_placeholders(self) -> None:
        self.assertEqual(local_cli.main(["harness", "create"]), 0)
        self.assertEqual(local_cli.main(["eval", "patch-quality"]), 0)


class ServerCliSmokeTests(unittest.TestCase):
    def test_server_commands_are_discoverable(self) -> None:
        parser = server_cli.build_parser()
        help_text = parser.format_help()

        for command in ["inventory", "blueprints", "manifest"]:
            with self.subTest(command=command):
                self.assertIn(command, help_text)

    def test_nested_server_commands_run_as_placeholders(self) -> None:
        self.assertEqual(server_cli.main(["inventory", "--fixture", "synthetic-company"]), 0)
        self.assertEqual(server_cli.main(["blueprints", "recommend"]), 0)
        self.assertEqual(server_cli.main(["manifest", "validate"]), 0)
        self.assertEqual(server_cli.main(["manifest", "compile", "--target", "github-actions"]), 0)


if __name__ == "__main__":
    unittest.main()
