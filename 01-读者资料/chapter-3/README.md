# 第3章：大模型实操指南

> **📍 来源**：第3章 全章内容
> **📄 行号**：第 1-297039 行
> **📖 页码**：第 XX-XX 页

---

## 章节简介

本章是实操指南，涵盖本地化部署、RAG 平台、文生图/视频、智能体框架等内容。

## 目录结构

```
chapter-3/
├── README.md                    # 本文件
├── deployment/                  # 部署相关
│   ├── ollama-setup.md         # Ollama 部署指南
│   ├── local-clients.md        # 本地化客户端
│   └── rag-platforms.md        # RAG 平台
├── prompts/                     # Prompt 汇编
│   ├── text-to-image/          # 文生图
│   ├── text-to-video/          # 文生视频
│   └── ai-tools/               # AI 工具
├── code/                        # 代码示例
│   ├── metagpt/                # MetaGPT
│   ├── flask-api/              # Flask API
│   ├── solidity/               # 智能合约
│   └── scripts/                # 脚本
└── tools/                       # 工具介绍
    ├── ima/                    # IMA 知识库
    ├── fastgpt/                # FastGPT
    └── n8n/                    # N8N 工作流
```

## 本章涵盖内容

### 3.1 本地化部署与 API 操作
- Ollama 本地部署
- 第三方 API（硅基流动等）
- 本地化 AI 客户端（Cherry Studio、AnythingLLM、Chatbox）

### 3.2 RAG 平台
- IMA（腾讯）
- FastGPT
- RAGFlow

### 3.3 文生图
- Gemini 2.0
- 即梦AI
- GPT-4o

### 3.4 文生视频
- 可灵 AI
- 即梦AI
- Sora

### 3.5 智能体框架
- MetaGPT
- Coze
- Dify

### 3.6 工作流自动化
- N8N

## 学习目标

1. 掌握大模型本地化部署方法
2. 了解主流 RAG 平台的使用
3. 学会使用文生图/视频工具
4. 熟悉智能体开发框架

## 实用工具对比

### 本地化客户端对比

| 工具 | 特点 | 适用场景 |
|------|------|----------|
| Cherry Studio | 多模型集成、知识库 | 个人全能助手 |
| AnythingLLM | 企业级知识库 | 中小企业 |
| Chatbox | 轻量级、跨平台 | 个人用户 |

### RAG 平台对比

| 平台 | 特点 | 适用场景 |
|------|------|----------|
| IMA | 微信生态集成 | 中文内容创作 |
| FastGPT | 开源、可视化 | 技术团队 |
| RAGFlow | 企业级深度解析 | 大型企业 |

## 快速开始

### Ollama 快速部署

```bash
# 安装后运行
ollama run deepseek-r1:7b
```

### IMA 使用流程

1. 下载 IMA 客户端
2. 微信扫码登录
3. 创建知识库
4. 上传文档或添加网页
5. 开始对话

## 知识点

- **本地化部署**：将大模型部署在本地设备
- **RAG**：检索增强生成
- **文生图**：AI 生成图片
- **文生视频**：AI 生成视频
- **工作流**：自动化任务流程
