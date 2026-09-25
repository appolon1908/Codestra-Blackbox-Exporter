#!/usr/bin/env python3
"""Fail closed unless the Blackbox runtime image is an immutable digest."""

from __future__ import annotations

import argparse
import os
import pathlib
import json
import re
import sys
from collections.abc import Mapping


IMAGE_REFERENCE = re.compile(
    r"^(?:[a-z0-9.-]+(?::[0-9]+)?/)?"
    r"[a-z0-9]+(?:[._-][a-z0-9]+)*"
    r"(?:/[a-z0-9]+(?:[._-][a-z0-9]+)*)*"
    r"@sha256:[0-9a-f]{64}$"
)
ROOT = pathlib.Path(__file__).resolve().parents[1]
LOCK = ROOT / "codestra/release/runtime-image.lock.json"
COMPOSE_SOURCES = (
    ROOT / "deploy/compose.yaml",
    ROOT / "codestra/runtime-v1/compose.yaml",
    ROOT / "codestra/runtime-v1/compose-codestra.yaml",
)


def load_env(path: pathlib.Path) -> dict[str, str]:
    values: dict[str, str] = {}
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        print(f"BLACKBOX_DEPLOYMENT_INPUT_ERROR=cannot read {path}: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
    for line_number, raw in enumerate(lines, 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            print(
                f"BLACKBOX_DEPLOYMENT_INPUT_ERROR={path}:{line_number}: expected KEY=VALUE",
                file=sys.stderr,
            )
            raise SystemExit(1)
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values


def validate(values: Mapping[str, str]) -> int:
    if values.get("BLACKBOX_EXPORTER_IMAGE"):
        print(
            "BLACKBOX_DEPLOYMENT_INPUT_ERROR=BLACKBOX_EXPORTER_IMAGE is fixed "
            "by the reviewed runtime lock and may not be caller-overridden",
            file=sys.stderr,
        )
        return 1
    try:
        lock = json.loads(LOCK.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"BLACKBOX_DEPLOYMENT_INPUT_ERROR=invalid runtime lock: {exc}", file=sys.stderr)
        return 1
    image = lock.get("image", "")
    if not IMAGE_REFERENCE.fullmatch(image) or lock.get("productionActivation") is not False:
        print("BLACKBOX_DEPLOYMENT_INPUT_ERROR=invalid immutable runtime lock", file=sys.stderr)
        return 1
    for path in COMPOSE_SOURCES:
        matches = re.findall(r"(?m)^\s+image:\s*(\S+)\s*$", path.read_text(encoding="utf-8"))
        if matches != [image]:
            print(
                f"BLACKBOX_DEPLOYMENT_INPUT_ERROR={path.relative_to(ROOT)} does not match runtime lock",
                file=sys.stderr,
            )
            return 1
    print("BLACKBOX_DEPLOYMENT_INPUTS_VALID=1")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--env-file", type=pathlib.Path)
    args = parser.parse_args()
    values: Mapping[str, str] = load_env(args.env_file) if args.env_file else os.environ
    return validate(values)


if __name__ == "__main__":
    raise SystemExit(main())
