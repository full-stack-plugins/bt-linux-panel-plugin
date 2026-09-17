# Codex 宝塔面板插件

> 通过 MCP 协议远程操作宝塔（BT）Linux 面板 13.0：诊断网站、审计安全、调用 98 个面板工具。

[English](README.md)

`bt-linux-panel` 让 Codex 通过 MCP 协议操作远程宝塔（BT）Linux 面板。Agent 不是用 SSH 跑通用 shell，而是路由到一个结构化的 98 工具面板（覆盖网站/数据库/服务/Docker/防火墙/SSL/计划任务/通知）。

本插件**不带本地 MCP server**，只交付技能 + 命令 + 钩子。你提供远程宝塔 MCP 端点（8765 + Bearer Token），Agent 提供路由。

## 适合谁

- 用宝塔面板管理 Linux、希望用自然语言让 AI 诊断与操作的运维人员。
- 同时管理多台宝塔面板的 Codex/ZCode/Kimi/Claude Code 用户，需要统一工作流。
- 想要可审计、有授权门控的操作（而非自由 shell）的 SRE。

## 解决什么问题

| 问题 | 本插件提供 | 可验证入口 |
|---|---|---|
| 网站故障或响应慢 | `bt-site-check` 命令 → nginx/PHP-FPM/MySQL 5 步诊断 | `skills/bt-site-ops/SKILL.md` |
| 不知道服务器安全状况 | `bt-security-scan` 命令 → 6 维度审计 | `skills/bt-security-audit/SKILL.md` |
| 端口 X 为什么不通 | `bt-firewall-audit` 命令 → 自动识别 firewalld/ufw/iptables | `skills/bt-firewall-audit/SKILL.md` |
| MCP 配置一头雾水 | `bt-mcp-setup` 命令 → 5 步安装 + 4 客户端配置 | `skills/bt-mcp-setup/SKILL.md` |
| 98 个工具不知用哪个 | `bt-mcp-tools` 命令 → 分类速查 + 风险等级 | `skills/bt-mcp-tools/SKILL.md` |
| 跨域综合工单 | `bt-diagnose` 命令 → 路由到对应专项 skill | `commands/bt-diagnose.md` |

## 架构

```text
用户输入
    │
    ▼
┌──────────────────────────────────────────────────────────────┐
│ bt-linux-panel                                                      │
│  ① SessionStart     hooks/env_check.py — 本地宝塔环境探测      │
│  ② UserPromptSubmit hooks/check_bt_intent.py — 意图识别        │
│  ③ /bt 命令          → bt-panel-ops skill → 跨域路由          │
│  ④ /bt-site-check    → bt-site-ops skill → 5 步诊断            │
│  ⑤ /bt-security-scan → bt-security-audit skill → 6 维审计     │
│  ⑥ /bt-firewall-audit → bt-firewall-audit skill               │
│  ⑦ /bt-mcp-setup     → bt-mcp-setup skill → MCP 配置指引       │
│  ⑧ /bt-mcp-tools     → bt-mcp-tools skill → 98 工具速查        │
└──────────────────────────────────────────────────────────────┘
    │
    ▼ (如已配置 MCP)
远程宝塔 13.0 面板 @ 8765 端口（Streamable HTTP + Bearer Token）
    │
    ▼
98 个面板工具（low 默认只读，medium/high 需用户明确授权）
```

| 属性 | 值 |
|---|---|
| 插件 ID（Codex） | `bt-linux-panel` |
| 插件 ID（ZCode / Kimi） | `bt` |
| 宿主兼容 | Codex CLI / ChatGPT 桌面应用、ZCode、Kimi Code CLI、Claude Code |
| 当前版本 | `1.0.0` |
| 插件清单 | `.codex-plugin/plugin.json`、`.zcode-plugin/plugin.json`、`kimi.plugin.json` |
| MCP server | **本插件不自带** — 远程宝塔在 `https://<ip>:8765/bt-mcp-<id>/mcp` 暴露 |
| 主要语言 | Python 3.13 钩子 + Markdown 技能 |
| 许可证 | Apache-2.0 |

## 兼容性

| 插件版本 | 宿主 | 宝塔面板 | 平台 | 状态 |
|---|---|---|---|---|
| `1.0.0` | Codex CLI / ChatGPT 桌面 | 宝塔 13.0 + Python 3.13 + MCP 插件 | macOS / Linux / Windows | 结构已验证 |
| `1.0.0` | ZCode | 同上 | 同上 | 结构已验证 |
| `1.0.0` | Kimi Code CLI | 同上 | 同上 | 结构已验证 |

> 真正的 MCP 连通性验证需要一台装有 MCP 服务的宝塔 13.0 面板，且 8765 端口可达。

## 安装

### 1. 安装宝塔 13.0 与 MCP 服务

本插件**不**安装宝塔面板本身。请先独立安装宝塔，然后：

- 升级到宝塔 13.0（面板首页 → 更新，或全新安装 `http://download.bt.cn/install/install13.sh`）
- 升级 Python 到 3.13：`bash /www/server/panel/script/upgrade_py313_bundle.sh`
- 在面板 **软件商店** 安装 **宝塔 MCP 服务** 插件
- 面板防火墙与云安全组**两处**放行 8765 端口
- 在 MCP 插件的 **接入与体验** 页面添加 Agent 公网 IP 到白名单
- 获取 Bearer Token

完整流程见 `skills/bt-mcp-setup/SKILL.md`。

### 2. 安装本插件

**Codex**：

```bash
codex plugin marketplace add https://github.com/partme-ai/partme-bt-plugin.git --ref main
codex plugin add bt-linux-panel@partme-ai
```

**ZCode**：建立本地 marketplace 文件夹（含 `marketplace.json`），然后 设置 → 插件 → 创建 → 添加插件市场。

**Kimi Code CLI**：通过 `kimi.plugin.json` 注册，Kimi 插件管理器安装。

### 3. 配置 MCP 客户端

按 `skills/bt-mcp-setup/SKILL.md` 的 4 客户端示例配置（Codex / ZCode / Kimi / Claude Code）。

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

## 风险与安全

本插件**仅作指引**。不在本地执行代码，不带远程 shell，不存储凭据。

- **本地**操作：钩子仅检查 `/www/server/panel/` 是否存在、探测 MCP 端口可达性。**绝不写**面板文件。
- **远程**操作（经 MCP）：Agent 路由到 98 工具面板。`low` 只读；`medium` 创建/修改资源；`high` 删除或执行——`high` 工具每次必须用户明确授权。

技能中的模板变量（`{{OS_VERSION}}`、`{{CURRENT_TIME}}`、`{{PANEL_IP}}`、`{{PANEL_PORT}}`）让 Agent 能输出与当前环境匹配的诊断结论。

## 隐私

见 [PRIVACY.md](PRIVACY.md)。简要：无遥测、无广告、无宿主数据服务；钩子只检查本地文件与端口可达性；不带本地 MCP server，故不代理任何凭据。

## 条款

见 [TERMS.md](TERMS.md)。你需自行负责：宝塔面板自身的许可、配置、安全；任何 `medium`/`high` 操作前的备份；Bearer Token 保密。

## 相关项目

- [`partme-ai/workbuddy-agent-experts`](https://github.com/partme-ai/workbuddy-agent-experts) — Agent 团队（宝塔运维 + 8 专项专家），可在任意 Agent 宿主复用
- [`partme-ai/plugins`](https://github.com/partme-ai/plugins) — 中央市场（Codex / ZCode / Kimi / Claude 四端）

## 许可证

Apache-2.0。见 [LICENSE](LICENSE)。