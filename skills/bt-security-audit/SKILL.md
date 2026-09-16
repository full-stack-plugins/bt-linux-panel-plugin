---
name: bt-security-audit
description: 宝塔部署服务器的安全审计专家：检查异常进程、SUID 文件、Webshell、SSH 安全、登录日志、可疑定时任务、入侵迹象、密码策略。当用户希望对宝塔服务器做安全合规检查时使用本 skill。
metadata:
  category: 安全审计
  target: 宝塔部署的 Linux 服务器
---

# 宝塔服务器安全审计专家

## 审计流程（6 维度）

### 1. SSH 安全

```bash
# SSH 配置文件
grep -E "^PermitRootLogin|^PasswordAuthentication|^Port\s" /etc/ssh/sshd_config

# 推荐配置
# PermitRootLogin no        （禁用 root 登录）
# PasswordAuthentication no （禁用密码登录）
# Port 2222                  （修改默认端口）

# 检查 authorized_keys 异常
find / -name "authorized_keys" 2>/dev/null
cat /root/.ssh/authorized_keys
cat /home/*/.ssh/authorized_keys

# 最近登录记录
last -20
last -i  # 显示 IP

# 失败登录
grep "Failed password" /var/log/secure 2>/dev/null | tail -20
grep "Failed password" /var/log/auth.log 2>/dev/null | tail -20
```

### 2. 异常进程与 CPU 占用

```bash
# CPU TOP 进程
ps aux --sort=-%cpu | head -20

# 内存 TOP
ps aux --sort=-%rss | head -20

# 异常进程特征
ps aux | grep -E "kdevtmpfsi|xmrig|minerd|cryptonight|kinsing"
ps aux | grep -E "/tmp/|/dev/shm/" | grep -v "rpc.statd"

# 反弹 shell 特征
ps aux | grep -E "bash -i|bash -c|/dev/tcp|nc .*-e|curl.*\|bash"
```

### 3. SUID/SGID 文件扫描

```bash
# 找所有 SUID 文件
find / -perm -4000 -type f 2>/dev/null

# 重点排查（不在白名单内的）
find / -perm -4000 -type f 2>/dev/null | grep -v -E "^(/usr/bin|/usr/sbin|/bin/|/sbin/)"

# SGID
find / -perm -2000 -type f 2>/dev/null

# 无主文件（可能遗留的后门）
find / -nouser -o -nogroup 2>/dev/null
```

### 4. Webshell 扫描（PHP 重点）

```bash
# 最近修改的 PHP 文件（可能是植入的）
find /www/wwwroot -name "*.php" -mtime -7 -ls

# 大文件扫描（常见 Webshell 特征）
find /www/wwwroot -name "*.php" -size +100k -exec grep -l "eval\s*(\s*\\\$" {} \;

# eval/base64 关键字
find /www/wwwroot -name "*.php" -exec grep -l "eval\s*(\s*base64_decode\|@eval\|assert\s*(" {} \;

# 宝塔 WAF 日志（如果启用）
ls -la /www/wwwlogs/btwaf/
tail -100 /www/wwwlogs/btwaf/access.log
```

### 5. 定时任务审计

```bash
# root crontab
crontab -l -u root

# 所有用户的 crontab
for user in $(cut -f1 -d: /etc/passwd); do
    echo "=== $user ==="
    crontab -l -u $user 2>/dev/null
done

# 系统级 cron
ls -la /etc/cron.d/ /etc/cron.daily/ /etc/cron.hourly/ /etc/cron.weekly/ /etc/cron.monthly/

# systemd timer
systemctl list-timers --all

# 重点：找 wget/curl 的 cron（常见矿木马手法）
grep -rE "wget|curl" /etc/cron* /var/spool/cron/ 2>/dev/null
```

### 6. 关键文件权限与完整性

```bash
# 关键系统文件
ls -la /etc/passwd /etc/shadow /etc/sudoers /etc/ssh/sshd_config

# 应为：
# /etc/passwd         644 root
# /etc/shadow         640 root
# /etc/sudoers        440 root

# 最近被修改的关键文件
find /etc -mtime -3 -type f 2>/dev/null

# 宝塔面板文件
ls -la /www/server/panel/BTPanel/ /www/server/panel/class/

# 入侵痕迹：找最近新增的系统用户
awk -F: '$3 >= 1000 {print $1}' /etc/passwd
```

## 风险评级

| 风险等级 | 触发条件 |
|---------|---------|
| **🔴 紧急** | 挖矿进程活动、反弹 shell 进程、Webshell 已确认、可疑账户创建 |
| **🟠 高** | SUID 异常文件、SSH 弱配置、最近新增的用户、异常 cron |
| **🟡 中** | 弱密码、SSH 默认端口、未配置 fail2ban、PHP 文件权限过大 |
| **🟢 低** | 缺少审计日志、缺少监控告警、无备份策略 |

## 入侵响应清单（紧急情况）

1. **隔离**：立即 `iptables -I INPUT -s <attacker_ip> -j DROP`
2. **取证**：`dd if=/dev/sda of=/mnt/forensic.img` 保留磁盘镜像
3. **凭据轮换**：所有用户密码、SSH 密钥、宝塔面板密码、API Token
4. **后门清理**：清理发现的 Webshell、可疑 cron、异常进程
5. **补丁**：升级所有软件版本、关闭未使用端口
6. **加固**：启用 fail2ban、配置 IP 白名单、启用宝塔 WAF
7. **复盘**：写入侵时间线、影响评估、修复证据

## MCP 集成工具

- `SecurityCheck`：安全评分、10 项检查、SSH 危险命令历史（low，一键可用）

## 输出模板

```
# 安全审计报告

## 整体评级
- 评分：X / 100
- 风险等级：🔴紧急 / 🟠高 / 🟡中 / 🟢低

## 关键发现（按风险排序）
1. [🔴] 发现 X 项：xxx
2. [🟠] 发现 X 项：xxx
...

## 详细审计结果

### 1. SSH 安全
- 状态：✅ 通过 / ❌ 不通过
- 证据：xxx
- 建议：xxx

### 2. 异常进程
- ...

## 修复优先级
1. [立即] ...
2. [24h 内] ...
3. [本周] ...
```