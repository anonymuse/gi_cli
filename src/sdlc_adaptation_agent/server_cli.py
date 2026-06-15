"""Command surface for the server-side SDLC agent."""

from __future__ import annotations

import argparse
import json
import sys

from .blueprints import recommend_blueprints
from .inventory import inventory_fixture
from .manifest import ManifestError, compile_manifest_file, validate_manifest_file


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="sdlc-server",
        description="Server-side CLI for fixture-backed portfolio SDLC inventory workflows.",
    )
    subcommands = parser.add_subparsers(dest="command")

    inventory = subcommands.add_parser("inventory", help="Inventory repositories from synthetic fixture data.")
    inventory.add_argument("--fixture", default="synthetic-company", help="Fixture id to inspect.")
    inventory.set_defaults(handler=_inventory)

    blueprints = subcommands.add_parser("blueprints", help="Recommend standardization blueprints.")
    blueprints_subcommands = blueprints.add_subparsers(dest="blueprints_command")
    recommend = blueprints_subcommands.add_parser("recommend", help="Recommend blueprints with evidence.")
    recommend.add_argument("--fixture", default="synthetic-company", help="Fixture id to inspect.")
    recommend.set_defaults(handler=_recommend)

    manifest = subcommands.add_parser("manifest", help="Validate or compile DeliveryManifest documents.")
    manifest_subcommands = manifest.add_subparsers(dest="manifest_command")
    validate = manifest_subcommands.add_parser("validate", help="Validate one DeliveryManifest.")
    validate.add_argument("path", help="Path to a DeliveryManifest JSON document.")
    validate.set_defaults(handler=_validate_manifest)
    compile_command = manifest_subcommands.add_parser("compile", help="Compile one DeliveryManifest to a target.")
    compile_command.add_argument("--target", default="github-actions", help="Compilation target.")
    compile_command.add_argument("path", help="Path to a DeliveryManifest JSON document.")
    compile_command.set_defaults(handler=_compile_manifest)

    return parser


def _inventory(args: argparse.Namespace) -> int:
    try:
        print(json.dumps(inventory_fixture(args.fixture), indent=2, sort_keys=True))
        return 0
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2


def _recommend(args: argparse.Namespace) -> int:
    try:
        print(json.dumps(recommend_blueprints(args.fixture), indent=2, sort_keys=True))
        return 0
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2


def _validate_manifest(args: argparse.Namespace) -> int:
    try:
        result = validate_manifest_file(args.path)
    except ManifestError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["valid"] else 1


def _compile_manifest(args: argparse.Namespace) -> int:
    try:
        print(compile_manifest_file(args.path, args.target), end="")
        return 0
    except ManifestError as exc:
        print(str(exc), file=sys.stderr)
        return 2


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not hasattr(args, "handler"):
        parser.print_help()
        return 0
    return args.handler(args)


if __name__ == "__main__":
    raise SystemExit(main())
