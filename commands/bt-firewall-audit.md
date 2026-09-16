---
description: 防火墙规则审计（自动识别 firewalld/ufw/iptables）：端口开放、IP 黑白名单、规则冲突、危险端口暴露（数据库/缓存对公网）。包含端口无法访问诊断流程。
argument-hint: ""
skills: bt-firewall-audit
---

Use the `bt-firewall-audit` skill for this request:

$ARGUMENTS

Auto-detect the firewall type, then audit (default policy → required ports → public exposure → IP allowlist → conflicts). Highlight any database/cache port exposed to 0.0.0.0 as 🔴 critical.