import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location("preflight", Path(__file__).parents[1] / "scripts" / "preflight_saved_crawl.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class Preflight(unittest.TestCase):
    def setUp(self):
        test_root = (Path(__file__).parents[1] / "runs" / "preflight-tests").resolve()
        test_root.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=test_root)
        assert Path(self.temp.name).resolve().is_relative_to(test_root)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def file(self, name, body=b"opaque test data; not a real SF crawl"):
        target = self.root / name
        target.write_bytes(body)
        return target

    def test_readiness_does_not_claim_valid_crawl_or_modify_file(self):
        target = self.file("保存 crawl.seospider")
        before = target.read_bytes()
        result = module.inspect_file(target)
        self.assertEqual(result["preflight_state"], "file_ready_unverified")
        self.assertEqual(result["load_state"], "not_attempted")
        self.assertEqual(target.read_bytes(), before)
        self.assertEqual(result["source"]["sha256"], module.inspect_file(target)["source"]["sha256"])

    def test_missing_empty_directory_and_config_errors(self):
        cases = [(self.root / "missing.seospider", "file_not_found"),
                 (self.file("empty.seospider", b""), "empty_file"),
                 (self.root, "not_a_file"),
                 (self.file("profile.seospiderconfig"), "configuration_not_crawl"),
                 (self.file("database.db"), "unsupported_file_type")]
        for path, code in cases:
            with self.subTest(code=code):
                self.assertEqual(module.inspect_file(path)["error"]["code"], code)

    def test_permission_failure_is_structured(self):
        target = self.file("saved.seospider")
        with patch.object(Path, "open", side_effect=PermissionError("denied")):
            self.assertEqual(module.inspect_file(target)["error"]["code"], "file_unreadable")

    def test_changed_content_has_different_fingerprint(self):
        target = self.file("saved.seospider")
        original = module.inspect_file(target)["source"]["sha256"]
        target.write_bytes(b"different saved content")
        self.assertNotEqual(module.inspect_file(target)["source"]["sha256"], original)


if __name__ == "__main__":
    unittest.main()
