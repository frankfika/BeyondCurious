# Ollama 本地化部署指南

> **📍 来源**：第3章 3.1.2 节「如何获取本地模型的API」
> **📄 行号**：第 4000-4500 行
> **📖 页码**：第 XX 页

---

## 什么是 Ollama？

Ollama 是主流的大模型本地化部署解决方案，支持 macOS、Linux、Windows，可运行 DeepSeek-R1、LLaMA、Qwen 等开源模型。

## 安装步骤

### 1. 下载安装

访问 [ollama.com](https://ollama.com) 下载对应系统的安装包。

### 2. 验证安装

```bash
ollama --version
```

### 3. 拉取模型

```bash
# 拉取 DeepSeek-R1 7B 版本
ollama pull deepseek-r1:7b

# 拉取 Qwen 2.5 7B 版本
ollama pull qwen2.5:7b
```

### 4. 运行模型

```bash
# 命令行提问方式
ollama run deepseek-r1:7b "你好，请介绍一下自己"

# 进入对话模式
ollama run deepseek-r1:7b
```

## 模型存储路径

- **UNIX-like 系统**：`~/.ollama/models`
- **Windows 系统**：`C:\Users\{username}\.ollama\models`

## API 使用

Ollama 默认在 `http://localhost:11434` 提供 API 服务。

### Python 调用示例

```python
import requests

response = requests.post('http://localhost:11434/api/generate', json={
    'model': 'deepseek-r1:7b',
    'prompt': '为什么天空是蓝色的？'
})

print(response.json()['response'])
```

## 常用命令

```bash
# 列出已下载的模型
ollama list

# 显示模型信息
ollama show deepseek-r1:7b

# 创建模型副本
ollama copy deepseek-r1:7b my-model

# 删除模型
ollama rm deepseek-r1:7b
```

## 硬件要求

| 组件 | 最低要求 | 推荐配置 |
|------|----------|----------|
| CPU | 4核心 | 8核心+ |
| 内存 | 8GB | 16GB+ |
| 存储 | 10GB 可用空间 | 50GB+ |
| GPU | 无 | 4GB+ VRAM |

## 支持的模型

- DeepSeek-R1 (1.5B, 7B, 8B, 14B, 32B, 70B)
- LLaMA 2/3
- Qwen 2.5
- Gemma
- Mistral
- Code Llama

## 注意事项

1. 7B 模型至少需要 8GB 内存
2. 14B 以上模型建议使用 GPU
3. 首次拉取模型需要下载时间
4. API 默认只监听本地，需修改配置才能远程访问
