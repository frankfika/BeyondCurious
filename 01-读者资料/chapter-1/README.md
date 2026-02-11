# 第1章：初识大模型

> **📍 来源**：第1章 全章内容
> **📄 行号**：第 1-1022 行
> **📖 页码**：第 1-XX 页

---

## 章节简介

本章介绍大模型的基础知识，包括大模型的定义、发展历程、智能体概念，以及主流大模型的对比测评。

## 目录结构

```
chapter-1/
├── README.md                           # 本文件
├── prompts/                             # Prompt 示例
│   ├── 01-math-test.md                 # 数学能力测试
│   ├── 02-travel-guide.md              # 旅游攻略生成
│   ├── 03-ielts-essay.md               # 雅思作文写作
│   └── 04-gaokao-essay.md              # 高考作文写作
└── knowledge/                           # 知识点总结
    └── key-concepts.md                  # 核心概念
```

## 本章涵盖内容

### 1.1 从ChatGPT到Manus AI
- 大模型的定义和核心概念
- Transformer 架构
- 涌现能力和上下文学习

### 1.2 大模型争霸战
- 主流大模型对比（GPT-4、DeepSeek、Claude、Qwen等）
- 不同场景测评（数学、旅游、雅思、高考作文）
- 模型选择指南

### 1.3 Token 机制
- Token 的定义和作用
- 中英文 Token 差异
- 成本优化策略

### 1.4 开源精神
- 开源大模型的发展
- DeepSeek、LLaMA 等开源模型

### 1.5 算力基础
- GPU/CPU 区别
- 算力衡量指标
- 硬件选择指南

## 学习目标

1. 理解大模型的基本原理
2. 了解主流大模型的特点和差异
3. 掌握 Token 计费机制
4. 学会选择合适的大模型

## Prompt 示例使用

### 数学测试 Prompt

```bash
cd prompts
cat 01-math-test.md
# 复制内容到大模型对话框
```

### 旅游攻略 Prompt

```bash
cat prompts/02-travel-guide.md
# 生成小红书风格旅游攻略
```

## 知识点

- **Transformer**：大模型的核心架构
- **涌现能力**：大模型规模达到一定程度后出现的新能力
- **Token**：大模型理解文本的基本单位
- **开源模型**：DeepSeek、LLaMA、Qwen 等
