---
description: 宝塔部署环境下的网站诊断：检查 Nginx/Apache/PHP-FPM/MySQL/SSL/响应慢/502/504/目录权限。适合"网站打不开/慢/报错"工单。
argument-hint: "[site_name]"
skills: bt-site-ops
---

Use the `bt-site-ops` skill for this request:

$ARGUMENTS

Run the 5-step diagnostic flow (health snapshot → nginx config audit → PHP-FPM state → MySQL slow queries → fix). Return a structured report with evidence and concrete fix commands.