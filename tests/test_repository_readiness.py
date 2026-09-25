from __future__ import annotations
import hashlib, importlib.util, json, subprocess, tarfile, tempfile, unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("inputs", ROOT / "scripts/validate_deployment_inputs.py"); assert SPEC and SPEC.loader
INPUTS = importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(INPUTS)
class ReadinessTests(unittest.TestCase):
    def test_validator(self) -> None: subprocess.run(["python3", "scripts/validate_repository_readiness.py"], cwd=ROOT, check=True)
    def test_image_override_is_rejected(self) -> None: self.assertEqual(INPUTS.validate({"BLACKBOX_EXPORTER_IMAGE": "example.invalid/x@sha256:" + "0" * 64}), 1)
    def test_fixed_inputs_pass(self) -> None: self.assertEqual(INPUTS.validate({}), 0)
    def test_bundle_is_deterministic(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            paths = [Path(directory) / name for name in ("one.tar.gz", "two.tar.gz")]
            for path in paths: subprocess.run(["python3", "scripts/build_config_bundle.py", "--output", str(path)], cwd=ROOT, check=True)
            self.assertEqual(hashlib.sha256(paths[0].read_bytes()).digest(), hashlib.sha256(paths[1].read_bytes()).digest())
            manifest = json.loads((ROOT / "codestra/release/config-bundle.manifest.json").read_text())
            with tarfile.open(paths[0], "r:gz") as archive: names = set(archive.getnames())
            self.assertEqual(names, set(manifest["files"]) | {"codestra/release/config-bundle.manifest.json"})
    def test_release_job_is_structurally_pinned(self) -> None:
        import yaml
        workflow = yaml.safe_load((ROOT / ".github/workflows/release-config-bundle.yml").read_text())
        job = workflow["jobs"]["release"]
        self.assertEqual(
            job["uses"],
            "appolon1908-hue/Codestra-Telemetry/.github/workflows/"
            "reusable-release-config-bundle.yml@"
            "777292781faeca9348d0e2ecdce6ac3f50c91d93",
        )
        self.assertEqual(job["with"]["component_id"], "blackbox-exporter")
    def test_vendored_upstream_is_byte_preserved(self) -> None:
        self.assertEqual((ROOT / ".gitattributes").read_text().splitlines()[-1], "upstream/** -whitespace")
if __name__ == "__main__": unittest.main()
