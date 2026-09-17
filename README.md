# Codex Baota Plugin

> Operate a remote Baota (BT) Linux panel 13.0 through the MCP protocol — diagnose sites, audit security, drive 98 panel tools.

[简体中文](README.zh-CN.md)

`bt-linux-panel` lets Codex operate a remote Baota (BT) Linux panel through the MCP protocol. Instead of generic shell commands against an SSH target, the agent routes to a structured 98-tool surface for sites, databases, services, Docker, firewall, SSL, cron, and notifications.

The plugin ships **no local MCP server**. It is a guidance + skills + commands layer. You bring the remote Baota MCP endpoint (port 8765, Bearer Token), the agent brings the routing.

## Who it's for

- Linux operators running a Baota panel who want AI-assisted diagnosis and operations through natural language.
- Codex/ZCode/Kimi/Claude Code users who manage many Baota panels and need a unified workflow.
- SREs who want consistent, auditable, authorization-gated operations instead of free-form shell.

## What it solves

| Problem | What this plugin provides | Verifiable entry |
|---|---|---|
| Site outage or slow response | `bt-site-check` command → nginx/PHP-FPM/MySQL 5-step diagnosis | `skills/bt-site-ops/SKILL.md` |
| Unknown security posture | `bt-security-scan` command → 6-dimension audit (SSH/process/SUID/webshell/cron/perm) | `skills/bt-security-audit/SKILL.md` |
| "Why is port X unreachable?" | `bt-firewall-audit` command → auto-detect firewalld/ufw/iptables | `skills/bt-firewall-audit/SKILL.md` |
| MCP setup confusion | `bt-mcp-setup` command → 5-step install + 4-client config examples | `skills/bt-mcp-setup/SKILL.md` |
| 98 tools, which one to call? | `bt-mcp-tools` command → categorized reference with risk levels | `skills/bt-mcp-tools/SKILL.md` |
| Cross-domain triage | `bt-diagnose` command → routes to the right specialist skill | `commands/bt-diagnose.md` |

## Architecture

```text
User prompt
    │
    ▼
┌──────────────────────────────────────────────────────────────┐
│ bt-linux-panel                                                      │
│  ① SessionStart    hooks/env_check.py — local BT panel probe  │
│  ② UserPromptSubmit hooks/check_bt_intent.py — intent detect  │
│  ③ /bt command      → bt-panel-ops skill → cross-domain router│
│  ④ /bt-site-check   → bt-site-ops skill → 5-step diagnose     │
│  ⑤ /bt-security-scan → bt-security-audit skill → 6-dim audit  │
│  ⑥ /bt-firewall-audit → bt-firewall-audit skill              │
│  ⑦ /bt-mcp-setup    → bt-mcp-setup skill → MCP wire guide     │
│  ⑧ /bt-mcp-tools    → bt-mcp-tools skill → 98-tool reference  │
└──────────────────────────────────────────────────────────────┘
    │
    ▼ (if MCP configured)
remote Baota 13.0 panel @ port 8765 (Streamable HTTP + Bearer Token)
    │
    ▼
98 panel tools (read-only by default; medium/high require explicit authorization)
```

| Property | Value |
|---|---|
| Plugin ID (Codex) | `bt-linux-panel` |
| Plugin ID (ZCode / Kimi) | `bt` |
| Host compatibility | Codex CLI / ChatGPT desktop, ZCode, Kimi Code CLI, Claude Code |
| Current version | `1.0.0` |
| Plugin manifests | `.codex-plugin/plugin.json`, `.zcode-plugin/plugin.json`, `kimi.plugin.json` |
| MCP server | **None shipped** — remote Baota panel exposes MCP at `https://<ip>:8765/bt-mcp-<id>/mcp` |
| Primary language | Python 3.13 hooks + Markdown skills |
| License | Apache-2.0 |

## Compatibility

| Plugin version | Host | Baota panel | Platform | Status |
|---|---|---|---|---|
| `1.0.0` | Codex CLI or ChatGPT desktop | Baota 13.0 + Python 3.13 + MCP plugin | macOS / Linux / Windows | Verified (structure) |
| `1.0.0` | ZCode | Baota 13.0 + Python 3.13 + MCP plugin | macOS / Linux / Windows | Verified (structure) |
| `1.0.0` | Kimi Code CLI | Baota 13.0 + Python 3.13 + MCP plugin | macOS / Linux / Windows | Verified (structure) |

> Live MCP verification requires a real Baota 13.0 panel with the MCP service installed and reachable on port 8765.

## Installation

### 1. Install Baota 13.0 and the MCP service

This plugin does **not** install the Baota panel itself. Install the panel separately, then:

- Update to Baota 13.0 (panel UI → Update, or fresh install from `http://download.bt.cn/install/install13.sh`)
- Upgrade Python to 3.13: `bash /www/server/panel/script/upgrade_py313_bundle.sh`
- Install the **宝塔 MCP 服务** plugin from the panel's software store
- Allow port 8765 in both panel firewall and cloud security group
- Add the Agent's public IP to the MCP plugin's whitelist
- Issue a Bearer Token from the **接入与体验** page

Full walkthrough: `skills/bt-mcp-setup/SKILL.md`.

### 2. Install the plugin

**Codex**:

```bash
codex plugin marketplace add https://github.com/partme-ai/partme-bt-plugin.git --ref main
codex plugin add bt-linux-panel@partme-ai
```

**ZCode**: create a local marketplace folder with a `marketplace.json` pointing at this repository, then add it via 设置 → 插件 → 创建 → 添加插件市场.

**Kimi Code CLI**: the plugin is registered via `kimi.plugin.json`; install via the Kimi plugin manager.

### 3. Configure the MCP client

Choose your client and follow the example in `skills/bt-mcp-setup/SKILL.md`:

```json
{
  "mcpServers": {
    "baota-mcp": {
      "url": "https://<面板公网IP>:8765/bt-mcp-<实例标识>/mcp",
      "headers": {
        "Authorization": "Bearer <授权令牌>"
      }
    }
  }
}
```

## What's inside

```
.codex-plugin/plugin.json        Codex manifest (name=bt-linux-panel)
.zcode-plugin/plugin.json        ZCode manifest (name=bt, userConfig)
kimi.plugin.json                  Kimi manifest (name=bt, hooks inline)
commands/                          7 slash-commands (双端共用)
  bt.md                            综合入口
  bt-diagnose.md                   跨域综合诊断
  bt-site-check.md                 网站诊断
  bt-security-scan.md             安全审计
  bt-firewall-audit.md            防火墙审计
  bt-mcp-setup.md                  MCP 接入指南
  bt-mcp-tools.md                  98 工具速查
hooks/                              advisory only, always exit 0
  hooks.json                       Claude-format (Codex + ZCode 共用)
  env_check.py                     SessionStart: 本地宝塔环境探测
  check_bt_intent.py               UserPromptSubmit: 意图识别
skills/                              6 SKILL.md packs
  bt-panel-ops/                    综合运维（跨域路由）
  bt-mcp-setup/                    MCP 接入配置（5 步 + 4 客户端示例）
  bt-mcp-tools/                    98 工具速查（19 类 + 风险等级）
  bt-site-ops/                     网站诊断（5 步 + 8 类问题修复）
  bt-security-audit/               安全审计（6 维度 + 入侵响应清单）
  bt-firewall-audit/               防火墙审计（自动识别 + 危险端口检测）
assets/                             logo.png, logo-dark.png, composer-icon.png (placeholder)
```

## Risk and authorization

This plugin is **advisory only**. It does not execute code locally, does not bundle a remote shell, and does not store credentials.

- **Local** operations: hooks inspect `/www/server/panel/` and detect MCP reachability. They emit Chinese summary lines for the agent to read. They never write to the panel.
- **Remote** operations via MCP: the agent routes to the 98-tool panel surface. `low` tools are read-only. `medium` tools have side effects (create/update resources). `high` tools delete or execute — the agent must confirm with the user each time before invoking.

The plugin honors the `{{OS_VERSION}}`, `{{CURRENT_TIME}}`, `{{PANEL_IP}}`, `{{PANEL_PORT}}` template variables in its skills so the agent can produce context-aware diagnostics.

## Privacy

See [PRIVACY.md](PRIVACY.md). In short:

- No telemetry, no advertising, no hosted data service.
- Hooks only inspect local filesystem (panel path, MCP port probe).
- The plugin does not contain a local MCP server, so it does not proxy any credentials.

## Terms

See [TERMS.md](TERMS.md). You are responsible for:

- The Baota panel's own license, configuration, and security posture.
- Backing up before any `medium`/`high`-risk operation.
- Keeping the Bearer Token secret (treat it like an API key).

## Related projects

- [`partme-ai/workbuddy-agent-experts`](https://github.com/partme-ai/workbuddy-agent-experts) — Agent team (BT operator + 8 specialists) reusable in any agent host
- [`partme-ai/plugins`](https://github.com/partme-ai/plugins) — Central marketplace (Codex / ZCode / Kimi / Claude)

## License

Apache-2.0. See [LICENSE](LICENSE).