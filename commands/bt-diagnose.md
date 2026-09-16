---
description: 宝塔服务器跨域综合诊断：自动从健康快照→服务→网站→数据库→防火墙→安全→计划任务→通知全链路扫描，输出统一诊断报告。
argument-hint: ""
skills: bt-panel-ops, bt-site-ops, bt-security-audit, bt-firewall-audit
---

Use the `bt-panel-ops` skill for cross-domain triage, then route to the right specialist:

$ARGUMENTS

Default flow:
1. Health snapshot (system + panel + services + network)
2. If "site slow/down" → `bt-site-ops`
3. If "security concern" → `bt-security-audit`
4. If "port access" → `bt-firewall-audit`
5. If MCP is configured → use `bt-mcp-tools` to select panel-native tools

Output a unified report at the end with risk-rated findings and prioritized fix steps.