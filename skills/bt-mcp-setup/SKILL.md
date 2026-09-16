---
name: bt-mcp-setup
description: 宝塔 Linux 面板 13.0 的 MCP 协议接入指南。覆盖安装前置、8765 端口放行、IP 白名单、Codex/ZCode/Kimi/Claude Code 的 MCP 客户端配置示例、Bearer Token 鉴权、HTTPS 证书要求、错误排查表。当用户希望把 AI 编码助手接入宝塔面板、用自然语言远程操作 98 个面板工具时使用本 skill。
metadata:
  category: MCP 整合
  target: 宝塔面板 13.0 + AI Agent (Codex/ZCode/Kimi/Claude Code)
---

# 宝塔面板 MCP 整合安装与配置

## 安装前置要求

- 已有宝塔面板 13.0 正式版（首页右上角【更新】升级）
- 服务器终端权限（root 或 sudo）
- Python 运行环境：3.13
- Agent（Codex/ZCode/Kimi）需支持远程 MCP 服务连接（Streamable HTTP）
- Agent 网络可达服务器的 **8765** 端口（TCP）
- 拥有面板管理员账号

## 安装步骤（5 步）

### 步骤 1：更新面板与 Python

```bash
# 升级到 13.0 正式版（面板首页右上角【更新】）

# 全新安装 13.0
curl -sSO http://download.bt.cn/install/install13.sh && bash install13.sh

# 在非面板终端升级 Python 到 3.13
bash /www/server/panel/script/upgrade_py313_bundle.sh
```

### 步骤 2：安装宝塔 MCP 服务

- 登录宝塔面板 → **软件商店** → 搜索"宝塔 MCP" → 找到【宝塔 MCP 服务】→ **安装**

### 步骤 3：放行 8765 端口（必须两处都放行）

**3a. 宝塔面板防火墙**：**安全**页面 → 入站规则 → 添加
- 协议：TCP
- 端口：8765
- 策略：accept

**3b. 云服务器厂商安全组/防火墙**：登录云厂商控制台，安全组添加入站规则同上

> ⚠️ 安全建议：仅放通 Agent 固定公网出口 IP，避免对所有来源开放（0.0.0.0/0）。

### 步骤 4：设置 IP 白名单

- MCP 插件 → **接入与体验** → 添加 Agent 公网出口 IP
- 仅支持**单个公网 IP**，不支持 IP 段
- Agent 公网 IP 可通过 `curl ifconfig.me` 查询

### 步骤 5：配置 Agent（不同客户端配置文件不同）

**方式 A：自动配置（推荐）**

- 接入与体验页面生成安装提示词 → 复制 → 发给 Agent
- Agent 会自动完成对应配置文件

**方式 B：手动配置**

参考 JSON 配置（Codex 风格）：

```json
{
  "mcpServers": {
    "baota-mcp": {
      "url": "https://<面板公网IP>:8765/bt-mcp-<实例标识>/mcp",
      "headers": {
        "Authorization": "Bearer <授权令牌>"
      },
      "disabled": false
    }
  }
}
```

**Codex 端**：`~/.codex/config.toml`

```toml
[mcp_servers.baota-mcp]
url = "https://<面板公网IP>:8765/bt-mcp-<实例标识>/mcp"

[mcp_servers.baota-mcp.headers]
Authorization = "Bearer <授权令牌>"
```

**ZCode/Kimi/Claude Code**：`~/.claude/mcp.json` 或插件配置

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

## 关键参数与连接信息

| 项目 | 值/说明 |
|------|---------|
| 服务端口 | **8765**（TCP） |
| 传输协议 | HTTPS（Streamable HTTP） |
| 鉴权方式 | **Bearer Token**（`Authorization` 请求头） |
| 接入路径 | `/bt-mcp-<实例标识>/mcp` |
| 实例标识 | 安装时生成（每个面板实例唯一） |
| 公网要求 | 需 HTTPS 证书（可用面板 SSL 申请 IP 证书） |

## HTTPS 证书要求

部分系统要求有效 HTTPS 证书链。申请可信 IP 证书路径：

- 面板 → **设置** → **安全设置** → **面板 SSL** → 打开面板 SSL → 选择 **IP 证书申请入口**

> 不要关闭 HTTPS 证书校验；不要使用自签名证书（Agent 会拒绝）。

## 首次只读验证指令

让 Agent 执行：

```
查看服务器当前状态，只读取 CPU、内存、磁盘、系统负载和服务运行情况，不要修改任何配置。
```

预期：Agent 返回结构化的服务器健康报告，未触发任何修改操作。

## 常见错误排查表

| 错误 | 原因 | 处理 |
|------|------|------|
| `403 ip denied` | Agent 公网 IP 未加入白名单 | 在白名单页面添加当前出口 IP |
| 提示词获取失败（证书链） | HTTPS 证书未生效 | 申请并安装面板 SSL 证书后重试 |
| 获取接入信息 HTTP 500 | Python 未升至 3.13 | 运行 `upgrade_py313_bundle.sh`，卸载重装 MCP 服务 |
| Agent 无法连接 | 端口未放行/网络不通 | 依次检查 8765 端口（防火墙+安全组）、IP 白名单、地址/令牌、SSL 证书有效性 |
| Codex 看不到 MCP 工具 | 配置文件未生效 | 重启 Codex，新建任务，输入 `/mcp` |
| Token 泄露怀疑 | 安全事件 | 立即在插件中重新生成授权，删除旧 Token，更新 Agent 配置 |

## 安全建议

1. **IP 白名单最小化**：仅放通必要 Agent IP，不开放 0.0.0.0/0
2. **生产环境先备份**：操作前备份数据库与站点文件
3. **凭证保密**：MCP 地址与令牌属敏感信息，避免提交至公开仓库
4. **不执行来源不明的命令**：AI Agent 建议的命令应人工复核后再执行
5. **高危操作保留人工确认**：删除文件、修改防火墙、重启服务等操作
6. **监控异常访问**：定期查看面板的 MCP 访问日志

## 模板变量（接入时由用户填写）

```yaml
panel_public_ip: <用户宝塔面板公网 IP>  # 例：203.0.113.10
panel_port: 8765                         # MCP 默认端口
panel_ssl_enabled: true                  # 是否启用面板 SSL
mcp_instance_id: <实例标识>              # 安装时生成
bearer_token: <授权令牌>                 # 接入与体验页面获取
agent_public_ip: <Agent 公网 IP>          # 通过 curl ifconfig.me 获取
```