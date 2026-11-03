#!/usr/bin/env python3
"""Validate Blackbox Exporter repository-only release readiness."""
from __future__ import annotations
import hashlib, json, re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
COMPOSE = ("deploy/compose.yaml", "codestra/runtime-v1/compose.yaml", "codestra/runtime-v1/compose-codestra.yaml")
REQUIRED = (".gitattributes", "README.md", "REPOSITORY_PROFILE.md", "SECURITY.md", ".github/CODEOWNERS", "docs/BACKUP_RESTORE_ROLLBACK.md", "docs/UPGRADE.md", "codestra/release/runtime-image.lock.json", "codestra/release/config-bundle.manifest.json", ".github/workflows/release-config-bundle.yml", "scripts/build_config_bundle.py", "requirements-validation.txt")
def fail(message: str) -> None: raise SystemExit(f"ERROR: {message}")
def load(path: str) -> dict:
    value = json.loads((ROOT / path).read_text())
    if not isinstance(value, dict): fail(f"{path} must contain an object")
    return value
def validate() -> None:
    missing = [path for path in REQUIRED if not (ROOT / path).is_file()]
    if missing: fail(f"missing readiness files: {missing}")
    if (ROOT / ".gitattributes").read_text().splitlines()[-1] != "upstream/** -whitespace": fail("vendored upstream whitespace boundary is missing")
    lock = load("codestra/release/runtime-image.lock.json"); image = lock.get("image", "")
    if not re.fullmatch(r"[a-z0-9./_-]+@sha256:[0-9a-f]{64}", image): fail("runtime image is mutable")
    if lock.get("binaryRevisionReadback") != lock.get("upstreamTagCommit"): fail("binary/source revision mismatch")
    if lock.get("productionActivation") is not False: fail("production activation must stay false")
    for relative in COMPOSE:
        source = (ROOT / relative).read_text()
        if re.findall(r"(?m)^\s+image:\s*(\S+)\s*$", source) != [image]: fail(f"{relative}: image mismatch")
        if re.search(r"(?m)^\s+ports\s*:", source): fail(f"{relative}: public port")
        if "cap_drop:\n      - ALL" not in source or "cap_add:\n      - NET_RAW" not in source: fail(f"{relative}: capability policy mismatch")
    for relative in ("config/blackbox.yml", "codestra/runtime-v1/blackbox.yml"):
        source = (ROOT / relative).read_text().lower()
        if "insecure_skip_verify: true" in source: fail(f"{relative}: insecure TLS")
    manifest = load("codestra/release/config-bundle.manifest.json")
    if manifest.get("component") != "blackbox-exporter" or manifest.get("productionActivation") is not False: fail("manifest identity/activation mismatch")
    files = manifest.get("files", {})
    if len(files) != 9: fail("manifest must contain nine governed files")
    for relative, expected in files.items():
        if not re.fullmatch(r"sha256:[0-9a-f]{64}", str(expected)) or "sha256:" + hashlib.sha256((ROOT / relative).read_bytes()).hexdigest() != expected: fail(f"checksum mismatch: {relative}")
    for workflow in (ROOT / ".github/workflows").glob("*.yml"):
        for reference in re.findall(r"(?m)^\s*(?:-\s*)?uses:\s*([^\s#]+)", workflow.read_text()):
            if not reference.startswith("./") and not re.fullmatch(r"[^@\s]+@[0-9a-f]{40}", reference): fail(f"mutable action: {workflow.name}: {reference}")
    caller = yaml.safe_load((ROOT / ".github/workflows/release-config-bundle.yml").read_text())
    release_job = caller.get("jobs", {}).get("release", {})
    authority = (
        "appolon1908-hue/Codestra-Telemetry/.github/workflows/"
        "reusable-release-config-bundle.yml@"
        "777292781faeca9348d0e2ecdce6ac3f50c91d93"
    )
    if release_job.get("uses") != authority: fail("release caller workflow authority mismatch")
    if release_job.get("with", {}).get("component_id") != "blackbox-exporter": fail("release caller component identity mismatch")
def main() -> None:
    validate(); print("BLACKBOX_EXPORTER_REPOSITORY_READINESS_SOURCE=PASS"); print("PRODUCTION_ACTIVATION=NO")
if __name__ == "__main__": main()
