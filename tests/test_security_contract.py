from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class SecurityContractTests(unittest.TestCase):
    def test_installer_guidance_uses_https_and_never_executes_download_inline(self) -> None:
        targets = [ROOT / "README.md", ROOT / "README.zh-CN.md", ROOT / "skills" / "bt-mcp-setup" / "SKILL.md"]
        for target in targets:
            text = target.read_text(encoding="utf-8")
            self.assertNotIn("http://download.bt.cn", text, target)
            self.assertIsNone(re.search(r"curl[^\n]*(?:\|\s*(?:ba)?sh|&&\s*(?:ba)?sh)", text), target)

    def test_installer_guidance_requires_integrity_verification(self) -> None:
        text = (ROOT / "skills" / "bt-mcp-setup" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("sha256", text.lower())
        self.assertIn("人工检查", text)

    def test_bearer_token_is_sensitive(self) -> None:
        manifest = json.loads((ROOT / ".zcode-plugin" / "plugin.json").read_text(encoding="utf-8"))
        self.assertIs(manifest["userConfig"]["bearer_token"].get("sensitive"), True)

    def test_host_manifests_are_version_aligned(self) -> None:
        codex = json.loads((ROOT / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8"))
        zcode = json.loads((ROOT / ".zcode-plugin" / "plugin.json").read_text(encoding="utf-8"))
        kimi = json.loads((ROOT / "kimi.plugin.json").read_text(encoding="utf-8"))
        self.assertEqual(zcode["version"], kimi["version"])
        self.assertTrue(codex["version"].startswith(zcode["version"] + "+codex."))


if __name__ == "__main__":
    unittest.main()
