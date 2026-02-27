---
section_id: B
title: 附录B：配置文件示例
status: draft
target_words: 1500
word_count: 1700
---

# 附录B：配置文件示例

本附录提供完整的 `openclaw.json` 配置文件示例，你可以根据自己的需求复制修改。

## 完整配置示例

```json
{
  "meta": {
    "version": "1.0.0",
    "created": "2026-01-15T10:00:00Z",
    "updated": "2026-01-20T15:30:00Z"
  },
  "general": {
    "timezone": "Asia/Shanghai",
    "locale": "zh-CN",
    "logLevel": "info"
  },
  "gateway": {
    "mode": "local",
    "bind": "loopback",
    "port": 18789,
    "auth": {
      "mode": "token",
      "token": "${OPENCLAW_TOKEN}"
    },
    "cors": {
      "enabled": true,
      "origins": ["http://localhost:3000", "http://127.0.0.1:3000"]
    }
  },
  "agents": {
    "defaults": {
      "model": {
        "primary": "anthropic/claude-3-5-sonnet-20240620"
      },
      "models": {
        "anthropic/claude-3-5-sonnet-20240620": {
          "alias": "main"
        },
        "anthropic/claude-3-opus-20240229": {
          "alias": "smart"
        },
        "openai/gpt-4o-mini": {
          "alias": "fast"
        },
        "ollama/qwen2.5-coder:32b": {
          "alias": "local"
        }
      },
      "workspace": "~/openclaw/workspace",
      "maxConcurrent": 4,
      "sandbox": {
        "mode": "non-main",
        "image": "openclaw/sandbox:latest",
        "workspaceAccess": "ro",
        "allowedTools": ["bash", "read", "write", "python"],
        "deniedTools": ["browser", "gateway", "cron"],
        "docker": {
          "cpuShares": 512,
          "memory": "512m",
          "networkMode": "none"
        }
      },
      "memory": {
        "enabled": true,
        "maxEntries": 1000,
        "autoSummarize": true
      }
    }
  },
  "models": {
    "providers": {
      "anthropic": {
        "apiKey": "${ANTHROPIC_API_KEY}",
        "models": [
          {
            "id": "claude-3-5-sonnet-20240620",
            "name": "Claude 3.5 Sonnet",
            "contextWindow": 200000
          },
          {
            "id": "claude-3-opus-20240229",
            "name": "Claude 3 Opus",
            "contextWindow": 200000
          }
        ]
      },
      "openai": {
        "apiKey": "${OPENAI_API_KEY}",
        "models": [
          {
            "id": "gpt-4o",
            "name": "GPT-4o",
            "contextWindow": 128000
          },
          {
            "id": "gpt-4o-mini",
            "name": "GPT-4o Mini",
            "contextWindow": 128000
          }
        ]
      },
      "deepseek": {
        "baseUrl": "https://api.deepseek.com/v1",
        "apiKey": "${DEEPSEEK_API_KEY}",
        "api": "openai-completions",
        "models": [
          {
            "id": "deepseek-chat",
            "name": "DeepSeek Chat",
            "contextWindow": 64000
          }
        ]
      },
      "bailian": {
        "baseUrl": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "apiKey": "${DASHSCOPE_API_KEY}",
        "api": "openai-completions",
        "models": [
          {
            "id": "qwen-max",
            "name": "通义千问 Max",
            "reasoning": false,
            "contextWindow": 262144
          }
        ]
      },
      "ollama": {
        "baseUrl": "http://127.0.0.1:11434/v1",
        "api": "openai-completions",
        "apiKey": "ollama",
        "models": [
          {
            "id": "qwen2.5-coder:32b",
            "name": "Qwen Local",
            "contextWindow": 32768
          }
        ]
      }
    }
  },
  "channels": {
    "telegram": {
      "enabled": true,
      "botToken": "${TELEGRAM_BOT_TOKEN}",
      "allowedUsers": [],
      "webhookUrl": ""
    },
    "whatsapp": {
      "enabled": false,
      "sessionName": "openclaw",
      "allowedNumbers": []
    },
    "discord": {
      "enabled": false,
      "botToken": "${DISCORD_BOT_TOKEN}",
      "allowedGuilds": [],
      "allowedChannels": []
    },
    "slack": {
      "enabled": false,
      "botToken": "${SLACK_BOT_TOKEN}",
      "appToken": "${SLACK_APP_TOKEN}",
      "allowedWorkspaces": []
    }
  },
  "hooks": {
    "preExecution": [],
    "postExecution": [],
    "onError": []
  },
  "skills": {
    "registry": "https://clawdhub.com",
    "autoUpdate": true,
    "trustedAuthors": ["openclaw-official"]
  }
}
```

## 配置项说明

### meta（元信息）

| 字段 | 说明 | 示例 |
|-----|------|------|
| `version` | 配置文件版本 | `"1.0.0"` |
| `created` | 创建时间（ISO 8601） | `"2026-01-15T10:00:00Z"` |
| `updated` | 更新时间（ISO 8601） | `"2026-01-20T15:30:00Z"` |

### general（通用设置）

| 字段 | 说明 | 可选值 |
|-----|------|--------|
| `timezone` | 时区设置 | `"Asia/Shanghai"`, `"America/New_York"` |
| `locale` | 语言区域 | `"zh-CN"`, `"en-US"` |
| `logLevel` | 日志级别 | `"debug"`, `"info"`, `"warn"`, `"error"` |

### gateway（Gateway配置）

| 字段 | 说明 | 可选值 |
|-----|------|--------|
| `mode` | 运行模式 | `"local"`, `"remote"` |
| `bind` | 绑定地址 | `"loopback"`（仅本机）, `"lan"`（局域网） |
| `port` | 监听端口 | `18789`（默认） |
| `auth.mode` | 认证模式 | `"token"`, `"none"` |
| `auth.token` | 访问令牌 | 建议使用环境变量 |

### agents（Agent配置）

| 字段 | 说明 | 示例 |
|-----|------|------|
| `model.primary` | 默认模型 | `"anthropic/claude-3-5-sonnet-20240620"` |
| `models` | 模型别名配置 | 见示例 |
| `workspace` | 工作目录 | `"~/openclaw/workspace"` |
| `maxConcurrent` | 最大并发数 | `4` |

### sandbox（沙箱配置）

| 字段 | 说明 | 可选值 |
|-----|------|--------|
| `mode` | 沙箱模式 | `"non-main"`, `"all"`, `"off"` |
| `image` | Docker镜像 | `"openclaw/sandbox:latest"` |
| `workspaceAccess` | 工作区权限 | `"ro"`（只读）, `"rw"`（读写） |
| `allowedTools` | 允许的工具 | `["bash", "read", "write"]` |
| `deniedTools` | 禁止的工具 | `["browser", "gateway"]` |

**沙箱模式说明**：

| 模式 | 说明 | 推荐场景 |
|-----|------|----------|
| `non-main` | 非主会话在Docker中运行 | 推荐，平衡安全与便利 |
| `all` | 所有会话在Docker中运行 | 最安全，操作本机受限 |
| `off` | 关闭沙箱 | 不推荐，仅调试使用 |

### models（模型配置）

支持多个模型提供商，每个提供商需要配置：

| 字段 | 说明 | 必需 |
|-----|------|------|
| `apiKey` | API密钥 | 是（除Ollama外） |
| `baseUrl` | 自定义API地址 | 否（国产模型需要） |
| `api` | API类型 | 否（默认openai-completions） |
| `models` | 模型列表 | 是 |

### channels（消息渠道配置）

#### Telegram

```json
{
  "telegram": {
    "enabled": true,
    "botToken": "${TELEGRAM_BOT_TOKEN}",
    "allowedUsers": ["username1", "username2"],
    "webhookUrl": "https://your-domain.com/webhook"
  }
}
```

#### WhatsApp

```json
{
  "whatsapp": {
    "enabled": true,
    "sessionName": "openclaw",
    "allowedNumbers": ["+86138xxxxxxxx"]
  }
}
```

#### Discord

```json
{
  "discord": {
    "enabled": true,
    "botToken": "${DISCORD_BOT_TOKEN}",
    "allowedGuilds": ["guild-id-1"],
    "allowedChannels": ["channel-id-1"]
  }
}
```

#### Slack

```json
{
  "slack": {
    "enabled": true,
    "botToken": "${SLACK_BOT_TOKEN}",
    "appToken": "${SLACK_APP_TOKEN}",
    "allowedWorkspaces": ["workspace-id-1"]
  }
}
```

## 环境变量文件示例

创建 `~/.openclaw/env` 文件：

```bash
# ============================================
# OpenClaw 环境变量配置
# ============================================

# Gateway 访问令牌（建议设置强密码）
OPENCLAW_TOKEN=your-secure-random-token-here

# ============================================
# AI 模型 API Keys
# ============================================

# Anthropic Claude
ANTHROPIC_API_KEY=sk-ant-api03-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# OpenAI
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# DeepSeek
DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# 阿里云百炼（通义千问）
DASHSCOPE_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# ============================================
# 消息平台 Tokens
# ============================================

# Telegram Bot Token
TELEGRAM_BOT_TOKEN=1234567890:ABCDEFGHIJKLMNOPQRSTUVWXYZ

# Discord Bot Token
DISCORD_BOT_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxx.xxxxxx.xxxxxxxxxxxxxxxxxxxxxxxxxxx

# Slack Tokens
SLACK_BOT_TOKEN=xoxb-xxxxxxxxxxxx-xxxxxxxxxxxx-xxxxxxxxxxxxxxxxxxxxxxxx
SLACK_APP_TOKEN=xapp-xxxxxxxxxxx-xxxxxxxxxxxxx-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# ============================================
# 第三方服务 API Keys
# ============================================

# GitHub
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Brave Search
BRAVE_SEARCH_API_KEY=BSxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# ============================================
# 代理设置（如需要）
# ============================================

# HTTP_PROXY=http://127.0.0.1:7890
# HTTPS_PROXY=http://127.0.0.1:7890
```

## 最小化配置示例

如果你只想快速启动，可以使用这个最小配置：

```json
{
  "gateway": {
    "auth": {
      "token": "${OPENCLAW_TOKEN}"
    }
  },
  "models": {
    "providers": {
      "anthropic": {
        "apiKey": "${ANTHROPIC_API_KEY}",
        "models": [
          {
            "id": "claude-3-5-sonnet-20240620",
            "name": "Claude 3.5 Sonnet"
          }
        ]
      }
    }
  }
}
```

配合环境变量：

```bash
OPENCLAW_TOKEN=your-token
ANTHROPIC_API_KEY=sk-ant-xxx
```

## 国产模型配置示例

### DeepSeek

```json
{
  "models": {
    "providers": {
      "deepseek": {
        "baseUrl": "https://api.deepseek.com/v1",
        "apiKey": "${DEEPSEEK_API_KEY}",
        "api": "openai-completions",
        "models": [
          {
            "id": "deepseek-chat",
            "name": "DeepSeek Chat",
            "contextWindow": 64000
          }
        ]
      }
    }
  }
}
```

### 通义千问

```json
{
  "models": {
    "providers": {
      "bailian": {
        "baseUrl": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "apiKey": "${DASHSCOPE_API_KEY}",
        "api": "openai-completions",
        "models": [
          {
            "id": "qwen-max",
            "name": "通义千问 Max",
            "reasoning": false,
            "contextWindow": 262144
          }
        ]
      }
    }
  }
}
```

### Ollama 本地模型

```json
{
  "models": {
    "providers": {
      "ollama": {
        "baseUrl": "http://127.0.0.1:11434/v1",
        "api": "openai-completions",
        "apiKey": "ollama",
        "models": [
          {
            "id": "qwen2.5-coder:32b",
            "name": "Qwen Local",
            "contextWindow": 32768
          }
        ]
      }
    }
  }
}
```

---

**提示**：修改配置文件后，记得重启Gateway使配置生效：

```bash
openclaw gateway restart
```
