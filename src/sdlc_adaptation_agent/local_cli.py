"""Placeholder command surface for the local workstation agent."""

from __future__ import annotations

import argparse


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="sdlc-local",
        description="Local workstation CLI for fixture-backed SDLC adaptation workflows.",
    )
    subcommands = parser.add_subparsers(dest="command")

    doctor = subcommands.add_parser("doctor", help="Inspect a fixture or local repository for safe findings.")
    doctor.set_defaults(handler=_placeholder("doctor"))

    explain = subcommands.add_parser("explain", help="Summarize repository purpose and safe first-change hints.")
    explain.set_defaults(handler=_placeholder("explain"))

    first_commit = subcommands.add_parser("first-commit", help="Guide a developer toward a first safe commit.")
    first_commit.set_defaults(handler=_placeholder("first-commit"))

    coach = subcommands.add_parser("coach", help="Explain human-led agentic coding practices.")
    coach.set_defaults(handler=_placeholder("coach"))

    harness = subcommands.add_parser("harness", help="Create or inspect a local agent harness.")
    harness_subcommands = harness.add_subparsers(dest="harness_command")
    harness_create = harness_subcommands.add_parser("create", help="Create a minimal policy-gated harness.")
    harness_create.set_defaults(handler=_placeholder("harness create"))

    eval_command = subcommands.add_parser("eval", help="Run local evaluation workflows.")
    eval_subcommands = eval_command.add_subparsers(dest="eval_command")
    patch_quality = eval_subcommands.add_parser("patch-quality", help="Score a patch using the MVP rubric.")
    patch_quality.set_defaults(handler=_placeholder("eval patch-quality"))

    return parser


def _placeholder(command_name: str):
    def handler(_: argparse.Namespace) -> int:
        print(f"sdlc-local {command_name}: placeholder command registered")
        return 0

    return handler


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not hasattr(args, "handler"):
        parser.print_help()
        return 0
    return args.handler(args)


if __name__ == "__main__":
    raise SystemExit(main())
