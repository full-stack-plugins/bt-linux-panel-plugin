#!/usr/bin/env python3
"""SessionStart hook: report Baota (BT) panel readiness for this plugin.

Advisory only — always exits 0. Stdout is a short Chinese summary intended
to be injected into session context by the host (Claude-format hooks).

Reports:
  1. Whether `bt` CLI exists on PATH (panel-side command)
  2. Whether the canonical panel path /www/server/panel/ is present
  3. Whether MCP port 8765 is reachable on the configured PANEL_PUBLIC_IP
     (if userConfig set the IP; otherwise skips the probe)

Exit 0 always — pure informational.
"""
from __future__ import annotations

import json
import os
import shutil
import socket
import sys
from pathlib import Path

PANEL_PATH = Path("/www/server/panel")
PANEL_PORT_FILE = PANEL_PATH / "data" / "port.pl"
MCP_PORT = 8765
MCP_TIMEOUT = 3.0


def find_bt_cli() -> str:
    found = shutil.which("bt") or shutil.which("BT")
    return found or ""


def find_panel_root() -> bool:
    return PANEL_PATH.is_dir()


def read_panel_port() -> int:
    if not PANEL_PORT_FILE.is_file():
        return 8888
    try:
        return int(PANEL_PORT_FILE.read_text(encoding="utf-8", errors="ignore").strip() or "8888")
    except ValueError:
        return 8888


def probe_mcp_port(host: str, port: int = MCP_PORT) -> bool:
    if not host:
        return False
    try:
        with socket.create_connection((host, port), timeout=MCP_TIMEOUT):
            return True
    except OSError:
        return False


def main() -> int:
    panel_present = find_panel_root()
    bt_cli = find_bt_cli()
    panel_port = read_panel_port()
    mcp_host = os.environ.get("BT_PANEL_IP", "").strip()
    mcp_up = probe_mcp_port(mcp_host) if mcp_host else None

    bits: list[str] = []
    if panel_present:
        bits.append(f"宝塔面板已检测（{panel_port} 端口）")
    else:
        bits.append("本地未发现宝塔面板（/www/server/panel/ 缺失）")
    if bt_cli:
        bits.append(f"`{Path(bt_cli).name}` CLI 在 PATH 中")
    else:
        bits.append("`bt` CLI 不在 PATH（不影响远端 MCP 模式）")
    if mcp_host:
        if mcp_up:
            bits.append(f"MCP 8765 端口可达（{mcp_host}）")
        else:
            bits.append(f"MCP 8765 端口不可达（{mcp_host}），检查面板防火墙与 IP 白名单")

    print(" | ".join(bits))
    return 0


if __name__ == "__main__":
    sys.exit(main())