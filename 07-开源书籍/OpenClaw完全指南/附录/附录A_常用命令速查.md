---
section_id: A
title: 附录A：常用命令速查
status: draft
target_words: 1500
word_count: 1600
---

# 附录A：常用命令速查

本附录汇总了OpenClaw最常用的CLI命令，方便你在使用过程中快速查阅。

## 安装与初始化

### 一键安装

```bash
# macOS / Linux / WSL2
curl -fsSL https://openclaw.ai/install.sh | bash

# Windows PowerShell
irm https://openclaw.ai/install.ps1 | iex
```

### NPM安装

```bash
# 全局安装
npm install -g openclaw@latest

# 使用国内镜像
npm config set registry https://registry.npmmirror.com
npm install -g openclaw@latest
```

### 初始化配置

```bash
# 启动初始化向导
openclaw onboard

# 初始化并注册为系统服务
openclaw onboard --install-daemon
```

## 服务管理

### 启动与停止

```bash
# 启动OpenClaw服务
openclaw start

# 停止OpenClaw服务
openclaw stop

# 查看运行状态
openclaw status

# 查看详细状态
openclaw gateway status
```

### Gateway管理

```bash
# 启动Gateway
openclaw gateway start

# 停止Gateway
openclaw gateway stop

# 重启Gateway
openclaw gateway restart

# 前台运行（调试用）
openclaw gateway --port 18789

# 查看Gateway日志
openclaw logs gateway
```

### 启动参数

```bash
# 指定端口
openclaw gateway --port 8080

# 指定绑定地址
openclaw gateway --bind 0.0.0.0

# 指定认证Token
openclaw gateway --token your-secure-token

# 允许未完全配置时启动
openclaw gateway --allow-unconfigured
```

## 配置管理

### 配置文件操作

```bash
# 查看配置文件路径
openclaw config path

# 打开配置文件
openclaw config

# 验证配置语法
openclaw config validate

# 查看完整配置
openclaw config show

# 查看特定部分
openclaw config show gateway
openclaw config show models
openclaw config show agents
```

### 环境变量

```bash
# 环境变量文件位置
~/.openclaw/env

# 重启后生效
openclaw gateway restart
```

## Skill管理

### 搜索与查看

```bash
# 列出所有可用Skills
openclaw skills list

# 列出已安装的Skills
openclaw skills list --installed

# 搜索Skills
openclaw skills search "email"
openclaw skills search weather

# 查看Skill详情
openclaw skills info weather-assistant

# 查看Skill依赖
openclaw skills info github --deps
```

### 安装与卸载

```bash
# 安装Skill
openclaw skills install weather-assistant

# 安装特定版本
openclaw skills install weather-assistant@2.0.0

# 安装最新版本
openclaw skills install weather-assistant@latest

# 从URL安装
openclaw skills install https://example.com/skills/my-skill.md

# 卸载Skill
openclaw skills uninstall weather-assistant

# 更新所有Skills
openclaw skills update

# 更新特定Skill
openclaw skills update weather-assistant
```

### 配置与测试

```bash
# 查看Skill配置选项
openclaw skills config weather-assistant --show

# 设置配置项
openclaw skills config weather-assistant set temperature_unit celsius

# 测试Skill
openclaw skills test weather-assistant

# 查看Skill日志
openclaw skills logs weather-assistant

# Skill授权（如OAuth）
openclaw skills auth gmail-manager
```

## 模型管理

### 模型配置

```bash
# 测试默认模型连接
openclaw model test

# 测试指定模型
openclaw model test anthropic/claude-3-5-sonnet-20240620

# 列出可用模型
openclaw model list

# 切换模型（在对话中使用）
/model fast
/model local
/model anthropic/claude-3-opus-20240229
```

## 工作流管理

### Lobster工作流

```bash
# 列出工作流
openclaw workflow list

# 运行工作流
openclaw workflow run my-workflow

# 验证工作流
openclaw workflow validate my-workflow

# 查看工作流日志
openclaw workflow logs my-workflow
```

## 调试与诊断

### 日志查看

```bash
# 查看所有日志
openclaw logs

# 查看Gateway日志
openclaw logs gateway

# 查看Agent日志
openclaw logs agent

# 实时跟踪日志
openclaw logs --follow

# 查看最近100行
openclaw logs --lines 100
```

### 缓存与清理

```bash
# 清除缓存
openclaw cache clear

# 清除Skill缓存
openclaw cache clear --skills

# 查看缓存大小
openclaw cache size
```

### 诊断工具

```bash
# 运行诊断检查
openclaw doctor

# 检查端口占用
lsof -i :18789

# 检查Node.js版本
node --version

# 检查OpenClaw版本
openclaw --version
openclaw -v
```

## 更新与卸载

### 更新OpenClaw

```bash
# 使用npm更新
npm update -g openclaw@latest

# 使用安装脚本更新
curl -fsSL https://openclaw.ai/install.sh | bash

# 更新后重启
openclaw gateway restart
```

### 卸载OpenClaw

```bash
# 停止服务
openclaw stop

# 卸载npm包
npm uninstall -g openclaw

# 删除配置文件（可选）
rm -rf ~/.openclaw

# 删除旧版配置（如有）
rm -rf ~/.clawdbot
```

## 快捷命令参考表

| 命令 | 功能 |
|-----|------|
| `openclaw start` | 启动服务 |
| `openclaw stop` | 停止服务 |
| `openclaw status` | 查看状态 |
| `openclaw gateway restart` | 重启Gateway |
| `openclaw config` | 打开配置文件 |
| `openclaw config validate` | 验证配置 |
| `openclaw logs` | 查看日志 |
| `openclaw skills list` | 列出Skills |
| `openclaw skills install <name>` | 安装Skill |
| `openclaw skills uninstall <name>` | 卸载Skill |
| `openclaw skills search <keyword>` | 搜索Skills |
| `openclaw skills test <name>` | 测试Skill |
| `openclaw model test` | 测试模型连接 |
| `openclaw doctor` | 运行诊断 |
| `openclaw cache clear` | 清除缓存 |

## 常用文件路径

| 文件/目录 | 路径 |
|----------|------|
| 主配置文件 | `~/.openclaw/openclaw.json` |
| 环境变量文件 | `~/.openclaw/env` |
| Skill目录 | `~/.openclaw/workspace/skills/` |
| 日志目录 | `~/.openclaw/logs/` |
| 缓存目录 | `~/.openclaw/cache/` |
| Agent工作区 | `~/.openclaw/workspace/` |
| SOUL.md | `~/.openclaw/workspace/SOUL.md` |
| MEMORY.md | `~/.openclaw/workspace/MEMORY.md` |

## 故障排查速查

### 端口被占用

```bash
# 查找占用18789端口的进程
lsof -i :18789

# 或
netstat -tlnp | grep 18789
```

### 权限问题

```bash
# 修复Skill目录权限
chmod -R 755 ~/.openclaw/workspace/skills

# 修复npm权限
mkdir ~/.npm-global
npm config set prefix '~/.npm-global'
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bashrc
source ~/.bashrc
```

### 命令未找到

```bash
# 检查npm全局路径
npm config get prefix

# 添加到PATH
export PATH="$(npm config get prefix)/bin:$PATH"
```

### 网络超时

```bash
# 设置代理
export HTTP_PROXY=http://127.0.0.1:7890
export HTTPS_PROXY=http://127.0.0.1:7890

# 然后重试安装
openclaw skills install weather-assistant
```

---

**提示**：大多数命令都支持 `--help` 参数查看详细用法，例如 `openclaw skills install --help`。
