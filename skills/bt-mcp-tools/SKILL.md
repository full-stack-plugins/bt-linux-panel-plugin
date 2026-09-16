---
name: bt-mcp-tools
description: 宝塔 Linux 面板 13.0 的 MCP 协议 98 个工具分类速查。按 19 个分类（基础/网站/网络/数据库/服务/Docker/系统/软件/防火墙/Java/Node/Python/Go/反代/HTML/SSH/安全/计划任务/通知）组织，每行标注工具名、风险等级、一句话功能、关键参数、与通用工具的映射。当 Agent 已接入 baota-mcp 通道、需要选择合适工具时使用本 skill。
metadata:
  category: 运维工具参考
  target: 宝塔面板 13.0 MCP 工具集
  count: 98
---

# 宝塔面板 MCP 工具速查表（98 工具）

## 通用约定

- **返回结构**：`{"status": bool, "msg": string, ...}`，失败 `status=false`
- **风险等级**：
  - `low` 只读查询（绿色）
  - `medium` 有副作用（黄色）
  - `high` 高危操作（红色，删除/覆盖/执行命令）
- 工具总数 98，按 19 类分组

---

## 一、基础工具（10 个，远程 Agent 专用）

| 工具 | 风险 | 功能 |
|------|------|------|
| `Read` | low | 读取文件（`file_path`, `offset`, `limit`） |
| `Edit` | high | 精确修改（`old_string`, `new_string`, `replace_all`） |
| `Write` | high | 写入/覆盖 |
| `Glob` | low | 按名查找文件 |
| `Grep` | low | 内容搜索（正则） |
| `LS` | low | 列目录 |
| `Bash` | high | 执行 Shell（`run_in_background`） |
| `BashStatus` | low | 查询后台任务 |
| `BashStop` | medium | 终止后台任务 |
| `Upload` | medium | 客户端上传文件 |

---

## 二、网站（15 个）

| 工具 | 风险 | 功能 |
|------|------|------|
| `SiteList` | low | 网站列表 |
| `SiteGetConfig` | low | 站点配置 |
| `SiteLogs` | low | 访问日志 |
| `SiteTraffic` | low | 站点流量 |
| `SiteCreate` | medium | 创建网站（`domain`, `port`, `php_version`） |
| `SiteDelete` | **high** | 删除网站 |
| `OneClickDeploy` | medium | 一键部署 CMS |
| `TrafficAnalysis` | low | 全站流量分析 |
| `SiteCertList` | low | 证书库列表 |
| `SiteSSLDeploy` | medium | 部署 SSL |
| `SiteSSLApply` | medium | 申请 SSL |
| `DomainManage` | **high** | 域名增删 |
| `SiteConfig` | medium | PHP/伪静态 |
| `SiteControl` | medium | 启停站点 |
| `SiteBackup` | medium | 备份站点 |

---

## 三、网络（3 个）

`WebFetch`（low）/ `ServerIP`（low）/ `Upload`（medium）

---

## 四、数据库（6 个）

| 工具 | 风险 | 功能 |
|------|------|------|
| `DatabaseList` | low | 数据库列表 |
| `DatabaseCreate` | medium | 创建（`name`, `db_user`, `password`） |
| `DatabaseDelete` | **high** | 删除 |
| `DatabaseBackup` | medium | 备份 |
| `MysqlQuery` | low | 只读 SQL |
| `MysqlExecute` | **high** | 写 SQL |

---

## 五、服务（2 个）

`ServiceStatus`（low）/ `ServiceControl`（medium）

---

## 六、Docker（10 个）

`ContainerList`（low）/ `ContainerLogs`（low）/ `ContainerInspect`（low）/ `ComposeList`（low）/ `ImageList`（low）/ `VolumeList`（low）/ `NetworkList`（low）/ `ContainerControl`（medium）/ `ContainerDelete`（**high**）/ `ImagePull`（medium）

---

## 七、系统（1 个）

`SystemInfo`（low）：CPU/内存/磁盘/负载/运行时长

---

## 八、软件商店（3 个）

`SoftwareList`（low）/ `SoftwareInstall`（medium）/ `SoftwareUninstall`（**high**）

---

## 九、防火墙（5 个）

`FirewallStatus`（low）/ `FirewallPortList`（low）/ `FirewallIpList`（low）/ `FirewallPortSet`（**high**）/ `FirewallIpSet`（**high**）

---

## 十、Java 项目（6 个）

`JavaJdk`（medium）/ `JavaProjectCreate`（medium）/ `JavaProjectInfo`（low）/ `JavaProjectControl`（medium）/ `JavaProjectModify`（medium）/ `JavaProjectDelete`（**high**）

---

## 十一、NodeJS 项目（6 个）

`NodeVersion`（medium）/ `NodeProjectCreate`（medium）/ `NodeProjectInfo`（low）/ `NodeProjectControl`（medium）/ `NodeProjectModify`（medium）/ `NodeProjectDelete`（**high**）

---

## 十二、Python 项目（8 个）

`PythonVersion`（medium）/ `PythonEnv`（medium）/ `PythonProjectCreate`（medium）/ `PythonProjectInfo`（low）/ `PythonProjectControl`（medium）/ `PythonProjectService`（medium）/ `PythonProjectModify`（medium）/ `PythonProjectDelete`（**high**）

---

## 十三、Go 项目（6 个）

`GoVersion`（medium）/ `GoProjectCreate`（medium）/ `GoProjectInfo`（low）/ `GoProjectControl`（medium）/ `GoProjectModify`（medium）/ `GoProjectDelete`（**high**）

---

## 十四、反向代理（5 个）

`ProxyProjectCreate`（medium）/ `ProxyProjectInfo`（low）/ `ProxyProjectModify`（medium）/ `ProxyWriteConfig`（medium）/ `ProxyProjectDelete`（**high**）

---

## 十五、HTML 静态项目（4 个）

`HtmlProjectInfo`（low）/ `HtmlProjectCreate`（medium）/ `HtmlProjectModify`（medium）/ `HtmlProjectDelete`（**high**）

---

## 十六、SSH（3 个）

`SSHInfo`（low）/ `SSHConfig`（**high**）/ `SSHIntrusion`（low）

---

## 十七、安全（1 个）

`SecurityCheck`（low）：安全评分、10 项检查、SSH 危险命令历史

---

## 十八、计划任务（2 个）

`GetCrontab`（low）/ `ManageCrontab`（**high**）

---

## 十九、通知（3 个）

`GetChannel`（low）/ `ManageChannel`（**high**）/ `SendMessage`（medium）

---

## 工具选择决策树

```
目标是什么？
├─ 只读查询
│  ├─ 本机 → 用通用工具（Bash + grep + read）更轻量
│  └─ 远端 → MCP low 工具
├─ 创建资源（站点/数据库/项目）
│  ├─ 本机 → 通用工具 + 手工命令
│  └─ 远端 → MCP medium 工具（先确认）
└─ 修改/删除资源
   ├─ 本机 → 通用工具（高危，需授权）
   └─ 远端 → MCP high 工具（**每次二次确认**）
```

## 风险等级速查

**只读**（low）：`SiteList` / `DatabaseList` / `SystemInfo` / `ServiceStatus` / `ContainerList` / `FirewallStatus` / `GetCrontab` / `GetChannel` / `TrafficAnalysis` / `*ProjectInfo` / `SSHInfo` / `SSHIntrusion` / `SecurityCheck`

**中风险**（medium）：`SiteCreate` / `DatabaseCreate` / `ServiceControl` / `SoftwareInstall` / `*ProjectCreate` / `*ProjectControl` / `*ProjectModify`（除 Delete）/ `SiteSSL*` / `SiteConfig` / `ContainerControl` / `ImagePull` / `BashStop` / `SendMessage` / `Upload`

**高风险**（high，每次必须用户明确确认）：`Edit` / `Write` / `Bash` / `SiteDelete` / `DomainManage` / `DatabaseDelete` / `MysqlExecute` / `ContainerDelete` / `SoftwareUninstall` / `FirewallPortSet` / `FirewallIpSet` / `*ProjectDelete` / `SSHConfig` / `ManageCrontab` / `ManageChannel`