# 第2章：大模型进阶指南

> **📍 来源**：第2章 全章内容
> **📄 行号**：第 1-1101 行
> **📖 页码**：第 XX-XX 页

---

## 章节简介

本章深入讲解提示词工程、RAG 与微调、三大协议（函数调用、MCP、A2A），以及 Markdown 语法。

## 目录结构

```
chapter-2/
├── README.md                    # 本文件
├── prompts/                     # Prompt 框架
│   ├── frameworks/              # 提示词框架
│   │   ├── 01-icio-framework.md
│   │   ├── 02-rise-framework.md
│   │   ├── 03-crispe-framework.md
│   │   ├── 04-broke-framework.md
│   │   └── 05-trace-framework.md
│   ├── techniques/              # 提示词技巧
│   │   ├── chain-of-thought.md
│   │   └── few-shot-learning.md
│   └── examples/                # 应用案例
│       ├── honglou-simulator.md
│       ├── ielts-teacher.md
│       └── mermaid-generator.md
├── code/                        # 代码示例
│   ├── basic_prompt.py          # 基础 Prompt 示例
│   └── rag_example.py           # RAG 示例
└── guides/                      # 指南
    ├── prompt-engineering.md     # 提示词工程指南
    └── markdown-syntax.md        # Markdown 语法
```

## 本章涵盖内容

### 2.1 提示词工程
- ICIO、RISE、CRISPE、BROKE、TRACE 框架
- 链式思考（CoT）
- 少样本学习
- 情感化交互

### 2.2 RAG 与微调
- RAG 原理与实现
- 微调的方法与场景
- RAG vs 微调选择策略

### 2.3 三大协议
- 函数调用（Function Call）
- MCP（Model Context Protocol）
- A2A（Agent to Agent）

### 2.4 Markdown 语法
- 基础语法
- Mermaid 图表
- 高级样式定制

## 学习目标

1. 掌握主流提示词框架
2. 理解 RAG 和微调的区别
3. 了解三大协议的应用场景
4. 熟练使用 Markdown

## 提示词框架对比

| 框架 | 全称 | 适用场景 | 复杂度 |
|------|------|----------|--------|
| ICIO | Instruction-Context-Input-Output | 数据处理 | 低 |
| RISE | Role-Input-Step-Expectation | 任务执行 | 中 |
| CRISPE | Capacity-Role-Insight-Statement-Personality-Experiment | 复杂任务 | 高 |
| BROKE | Background-Role-Objective-KeyResult-Evolve | 迭代优化 | 中 |
| TRACE | Task-Request-Action-Context-Example | 实际操作 | 中 |

## 知识点

- **提示词工程**：设计有效 Prompt 的技能
- **RAG**：检索增强生成
- **微调**：使用特定数据训练模型
- **MCP**：模型上下文协议
- **A2A**：智能体间通信协议
