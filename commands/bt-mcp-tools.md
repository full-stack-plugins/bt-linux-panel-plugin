---
description: 列出宝塔 MCP 协议的 98 个工具（按 19 类分组），给出风险等级（low/medium/high）和参数签名。当 Agent 已接入 baota-mcp 后需要选择合适工具时使用。
argument-hint: "[site|db|docker|firewall|ssl|cron|service|...]"
skills: bt-mcp-tools
---

Use the `bt-mcp-tools` skill for this request:

$ARGUMENTS

Return the matching tool category, the tool signature, and the risk level. Highlight any `high`-risk tool that needs explicit user authorization.