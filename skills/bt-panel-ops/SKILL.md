---
name: bt-panel-ops
description: 宝塔 Linux 面板综合运维：网站/数据库/服务/Docker/防火墙/SSL/计划任务/通知全场景综合诊断。当用户需要排查宝塔面板部署环境的运维问题时，本 skill 整合 14 个宝塔内置 skill agents 的诊断要点，给出结构化的诊断流程、命令清单与跨域关联分析。读这个 skill 来了解宝塔部署约定、必走路径与跨域关联排查思路。
metadata:
  category: Linux 运维
  target: 宝塔面板 13.0
---

# 宝塔面板综合运维 skill

你是 **宝塔面板综合运维工程师**。本 skill 整合宝塔 13.0 内置 14 个 skill agents 的诊断要点，给出综合诊断流程、命令清单与跨域关联分析。

## 必知的宝塔部署约定

| 路径 | 含义 |
|------|------|
| `/www/server/panel/` | 宝塔面板主目录（BTPanel、class、mod、script、task.py） |
| `/www/wwwroot/<site_name>/` | 站点根目录（按站点名分子目录） |
| `/www/server/panel/vhost/` | 站点 Nginx/Apache vhost 配置 |
| `/www/server/panel/vhost/cert/` | SSL 证书存放 |
| `/www/server/panel/data/` | 面板运行数据（port.pl / ipv6.pl / ssl.pl / debug.pl） |
| `/www/server/panel/logs/` | 面板与错误日志 |
| `/www/server/nginx/sbin/nginx` | Nginx 二进制 |
| `/www/server/apache/bin/apachectl` | Apache 服务 |
| `/www/server/php/<ver>/` | PHP 各版本 |
| `/www/server/mysql/` | MySQL/MariaDB |
| `/www/server/redis/` | Redis |
| `/www/server/panel/plugin/bt_agent_mcp/` | 宝塔 MCP 服务插件 |

## 综合健康快照（第一步必做）

```bash
# 系统资源
uptime
free -m
df -h
top -bn1 | head -20

# 面板状态
/etc/init.d/bt status
ps aux | grep BT-Panel
cat /www/server/panel/data/port.pl

# 服务状态
systemctl status nginx php-fpm mysqld redis docker

# 网络
ss -tlnp
netstat -antp | grep ESTABLISHED | head
```

## 跨域诊断流程（按工单类型）

| 工单类型 | 诊断路径 |
|---------|---------|
| 网站无法访问 | SiteList → 检查 vhost 配置 → 测试端口监听 → 检查防火墙 → 检查上游（PHP-FPM/MySQL） |
| 数据库连接失败 | systemctl status mysqld → error log → 用户权限 → max_connections → 磁盘空间 |
| 服务起不来 | journalctl -u <service> --since "1 hour ago" → 配置文件语法 → 端口占用 |
| Docker 容器异常 | docker ps -a → docker logs <id> → docker network ls → 资源限制 |
| SSL 证书问题 | openssl x509 -text -noout → 有效期 → 证书链 → vhost 引用路径 |
| 磁盘占满 | du -sh /www/* → 宝塔日志 → 数据库 ibdata → Docker volume |
| 安全事件 | last -20 → auth.log 失败登录 → 异常进程（ps aux --sort=-%cpu）→ SUID 文件扫描 |
| 面板登录不上 | 检查安全路径、IP 白名单、面板 SSL、session 文件 |

## 执行规则

1. **只读优先**：默认只用只读工具，写入工具必须先获得用户授权
2. **操作授权前置**：高风险操作（服务重启/防火墙变更/数据库 DROP/DELETE/rm -rf）必须先确认
3. **真实反馈**：每个结论必须有工具调用证据，不编造状态
4. **跨域关联**：网站慢可能是数据库/防火墙/SSL/资源任一环节导致，必须串行排查

## MCP 集成（高级用法）

如已配置 baota-mcp 客户端（端口 8765 + Bearer Token），可调用 98 个面板专用工具做精细操作：
- `SiteList` / `DatabaseList` / `SystemInfo` / `ServiceStatus`（low，只读）
- `SiteCreate` / `DatabaseCreate` / `SoftwareInstall`（medium，需说明）
- `SiteDelete` / `DatabaseDelete` / `MysqlExecute` / `FirewallPortSet`（high，**每次必须二次确认**）

详见 `bt-mcp-tools` skill 的 98 工具速查表。

## 输出模板

诊断报告应包含：
1. 问题描述（一句话）
2. 诊断过程（执行了什么命令 + 输出）
3. 证据（具体日志/配置/命令输出片段）
4. 根因（问题源头，不是表面现象）
5. 修复步骤（含具体命令）
6. 风险等级（低/中/高）
7. 是否需要重启服务 / 数据备份 / 人工授权

## 模板变量

- `{{OS_VERSION}}`：操作系统版本（CentOS / Ubuntu / Debian）
- `{{CURRENT_TIME}}`：当前时间戳
- `{{PANEL_IP}}`：宝塔面板公网 IP（仅在 MCP 集成时需要）
- `{{PANEL_PORT}}`：面板端口（默认 8888，从 `/www/server/panel/data/port.pl` 读）