"""Placeholder command surface for the server-side SDLC agent."""

from __future__ import annotations

import argparse


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="sdlc-server",
        description="Server-side CLI for fixture-backed portfolio SDLC inventory workflows.",
    )
    subcommands = parser.add_subparsers(dest="command")

    inventory = subcommands.add_parser("inventory", help="Inventory repositories from synthetic fixture data.")
    inventory.add_argument("--fixture", default="synthetic-company", help="Fixture id to inspect.")
    inventory.set_defaults(handler=_placeholder("inventory"))

    blueprints = subcommands.add_parser("blueprints", help="Recommend standardization blueprints.")
    blueprints_subcommands = blueprints.add_subparsers(dest="blueprints_command")
    recommend = blueprints_subcommands.add_parser("recommend", help="Recommend blueprints with evidence.")
    recommend.set_defaults(handler=_placeholder("blueprints recommend"))

    manifest = subcommands.add_parser("manifest", help="Validate or compile DeliveryManifest documents.")
    manifest_subcommands = manifest.add_subparsers(dest="manifest_command")
    validate = manifest_subcommands.add_parser("validate", help="Validate one DeliveryManifest.")
    validate.set_defaults(handler=_placeholder("manifest validate"))
    compile_command = manifest_subcommands.add_parser("compile", help="Compile one DeliveryManifest to a target.")
    compile_command.add_argument("--target", default="github-actions", help="Compilation target.")
    compile_command.set_defaults(handler=_placeholder("manifest compile"))

    return parser


def _placeholder(command_name: str):
    def handler(_: argparse.Namespace) -> int:
        print(f"sdlc-server {command_name}: placeholder command registered")
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
