---
name: bt-harness
description: "BT (宝塔) Linux panel calling spec: MCP-protocol panel operations (sites/daemons/security), credential handling, and the diagnose-first discipline. Read this before any panel operation."
---

# 宝塔面板调用规范

执行通道：经 MCP 协议操作宝塔（BT）Linux 面板（诊断/站点/守护进程/安全）。

## 1. 凭据与环境

- 面板地址 + API 凭据由 `bt-setup` 引导配置；凭据不进日志与产物清单。
- 面板版本 13.0 口径；其他版本行为差异如实上报。

## 2. 硬规则

- 先 `diagnose` 后操作：面板不可达/版本不符时不执行变更类动作。
- 变更类（站点/安全/守护进程）操作必须用户明确授权；查询类不受限。

## 3. 纪律

- 每步以工具返回为事实来源；操作失败原文上报。
- 不在参数里拼接未经验证的用户输入（面板注入面）。
