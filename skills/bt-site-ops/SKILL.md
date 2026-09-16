---
name: bt-site-ops
description: 宝塔部署环境下的网站诊断专家：分析 Nginx/Apache 配置、PHP-FPM、SSL 证书、数据库连接、响应慢、502/504、目录权限等问题。当用户报告"网站无法访问/慢/出错"且主机是宝塔部署时使用本 skill。
metadata:
  category: 网站运维
  target: 宝塔面板部署的网站（Nginx/Apache + PHP-FPM + MySQL）
---

# 宝塔网站诊断专家

## 诊断流程（5 步）

### 第一步：基础健康快照

```bash
# 系统级
uptime
free -m
df -h
top -bn1 | head -20

# 网站服务
systemctl status nginx
systemctl status php-fpm
systemctl status mysqld

# 网络监听
ss -tlnp | grep -E ':80|:443|:9000|:3306'
```

### 第二步：Nginx/Apache 配置审计

```bash
# vhost 配置位置
ls /www/server/panel/vhost/nginx/        # Nginx
ls /www/server/panel/vhost/apache/       # Apache

# 检查语法
nginx -t
apachectl configtest

# 检查关键配置项
grep -E "fastcgi_pass|root\s|listen\s|ssl_certificate" /www/server/panel/vhost/nginx/<site>.conf
```

### 第三步：PHP-FPM 状态

```bash
# 进程数
ps aux | grep php-fpm | wc -l

# 慢日志
ls -la /www/server/php/<ver>/var/log/
tail -100 /www/server/php/74/var/log/php-fpm.slow.log 2>/dev/null

# 错误日志
tail -100 /www/server/php/74/var/log/php-fpm.log

# 配置
grep -E "pm.max_children|pm.start_servers|request_terminate_timeout" /www/server/php/74/etc/php-fpm.conf
```

### 第四步：MySQL 慢查询

```bash
# 慢查询日志
ls -la /www/server/mysql/mysql<ver>.log
tail -100 /www/server/data/mysql-slow.log 2>/dev/null

# 进程列表
mysqladmin -uroot -p<pwd> processlist

# 关键配置
mysql -e "SHOW VARIABLES LIKE 'slow_query_log'"
mysql -e "SHOW VARIABLES LIKE 'max_connections'"
mysql -e "SHOW STATUS LIKE 'Threads_connected'"
```

### 第五步：综合分析与修复建议

## 常见问题与修复

### 502 Bad Gateway

**症状**：网站返回 502

**根因排查**：
1. PHP-FPM 未运行：`systemctl status php-fpm`
2. 端口未监听：`ss -tlnp | grep 9000`
3. vhost 中 fastcgi_pass 路径错误
4. PHP-FPM 进程数耗尽（`pm.max_children` 不够）

**修复**：
```bash
# 重启 PHP-FPM
systemctl restart php-fpm

# 调大进程数（按内存算：每进程约 30MB）
sed -i 's/pm.max_children = .*/pm.max_children = 50/' /www/server/php/74/etc/php-fpm.conf
systemctl reload php-fpm
```

### 网站响应慢

**诊断路径**：
1. **网络层**：用 `curl -w "time_total: %{time_total}\n" -o /dev/null -s <site>` 测试响应时间
2. **数据库层**：检查慢查询、连接数、锁等待
3. **PHP 层**：检查 PHP-FPM 慢日志、OPcache 是否启用
4. **磁盘层**：`iostat -x 1 5`、`iotop`
5. **应用层**：开启 XHProf / Tideways 跟踪

**常见优化**：
```bash
# 启用 OPcache
grep "opcache.enable" /www/server/php/74/etc/php.ini
# 应为 opcache.enable=1

# 检查静态资源缓存
grep -E "expires|cache-control" /www/server/panel/vhost/nginx/<site>.conf
```

### SSL 证书问题

```bash
# 检查证书有效期
openssl x509 -text -noout -in /www/server/panel/vhost/cert/<site>/fullchain.pem | grep -E "Not Before|Not After"

# 检查证书链
openssl s_client -connect <site>:443 -servername <site> < /dev/null 2>&1 | grep -E "Verify return code|subject=|issuer="

# Let's Encrypt 续签
certbot renew --dry-run
```

### 磁盘占满

```bash
# 找出大目录
du -sh /www/* | sort -hr | head -10
du -sh /www/wwwlogs/* | sort -hr | head -10  # 访问日志
du -sh /www/server/mysql/data/* | sort -hr | head -10  # 数据库

# 清理日志（保留最近 7 天）
find /www/wwwlogs -name "*.log" -mtime +7 -delete
```

## MCP 集成工具映射

如已接入 baota-mcp：
- `SiteList` → 列出所有站点
- `SiteGetConfig` → 取单个站点完整配置
- `SiteLogs` → 取访问/错误日志
- `SiteTraffic` → 取流量数据
- `SiteSSLDeploy` → 一键部署证书
- `SiteSSLApply` → 申请 Let's Encrypt

## 输出模板

诊断报告：
1. **症状**（用户报告的 + 你观察到的）
2. **证据**（命令输出片段、日志行、配置片段）
3. **根因**（指向具体配置项或资源瓶颈）
4. **修复步骤**（按风险从低到高排序）
5. **验证方法**（修复后如何确认问题解决）
6. **预防建议**（如何避免再次发生）