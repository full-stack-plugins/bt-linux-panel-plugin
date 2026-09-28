#!/usr/bin/env python3
"""UserPromptSubmit hook: detect when the user's prompt is about Baota.

Reads the user prompt from stdin (Claude-format hooks), scans for
Baota-related keywords, and emits a one-line advisory when matched.
Advisory only — exits 0; non-matching prompts produce no output.
"""
from __future__ import annotations

import json
import re
import sys

INTENT_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"宝塔|\bbt[\s_-]?panel\b|\bbaota\b", re.IGNORECASE),
    re.compile(r"宝塔\s*MCP|\bbt[\s_-]?mcp\b", re.IGNORECASE),
    re.compile(r"/www/server/panel|/www/wwwroot|bt\s+命令", re.IGNORECASE),
    re.compile(r"\bsite\.?(list|create|delete|ssl|cert)|站点(列表|创建|删除|SSL|证书)", re.IGNORECASE),
    re.compile(r"firewall.*(port|ip)|防火墙", re.IGNORECASE),
    re.compile(r"宝塔\s*(?:计划任务|docker|容器|ssl|证书|安全|备份|网站|数据库)"),
)


def match_intent(text: str) -> str | None:
    for pat in INTENT_PATTERNS:
        m = pat.search(text)
        if m:
            return m.group(0)
    return None


def main() -> int:
    try:
        raw = sys.stdin.read()
    except OSError:
        return 0
    if not raw:
        return 0

    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        return 0

    prompt = payload.get("prompt") or payload.get("text") or ""
    if not isinstance(prompt, str):
        return 0

    matched = match_intent(prompt)
    if not matched:
        return 0

    print(f"宝塔运维意图识别: `{matched}` — 已激活 bt-panel-ops 路由")
    return 0


if __name__ == "__main__":
    sys.exit(main())