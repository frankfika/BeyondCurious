# 《动手做 AI Agent：零基础玩转智能体》配套代码仓库

> **📖 书籍**：《动手做 AI Agent：零基础玩转智能体》
> **📅 版本**：v1.0
> **📁 组织方式**：按章节分类

---

## 简介

本仓库是《动手做 AI Agent：零基础玩转智能体》一书的配套代码仓库，所有内容按章节组织，方便读者按学习进度查找。

## 快速导航

### 📚 按章节浏览

| 章节 | 内容 | 文件数 |
|------|------|--------|
| [第1章：初识大模型](chapter-1/) | 大模型基础、主流模型对比、Token机制 | 4 |
| [第2章：大模型进阶指南](chapter-2/) | 提示词工程、RAG与微调、Markdown语法 | 8 |
| [第3章：大模型实操指南](chapter-3/) | 本地部署、文生图/视频、智能体框架 | 10 |

---

## 第1章：初识大模型

[点击进入 →](chapter-1/)

**主要内容：**
- 大模型的定义与发展历程
- 主流大模型对比（GPT-4、DeepSeek、Claude、Qwen等）
- Token 机制与成本优化
- 开源精神与算力基础

**Prompt 示例：**
- 数学能力测试
- 旅游攻略生成（小红书风格）
- 雅思作文写作
- 高考作文写作

---

## 第2章：大模型进阶指南

[点击进入 →](chapter-2/)

**主要内容：**
- 提示词工程框架（ICIO、RISE、CRISPE、BROKE、TRACE）
- 链式思考（CoT）推理方法
- RAG 与微调技术
- 三大协议（函数调用、MCP、A2A）
- Markdown 语法完整指南

**Prompt 框架：**
- ICIO 框架
- RISE 框架
- CRISPE 框架
- BROKE 框架
- 链式思考

**应用案例：**
- 红楼哄玉模拟器
- 雅思老师
- Mermaid 图表生成器

---

## 第3章：大模型实操指南

[点击进入 →](chapter-3/)

**主要内容：**
- Ollama 本地化部署
- RAG 平台（IMA、FastGPT、RAGFlow）
- 文生图/视频工具
- MetaGPT 智能体框架
- N8N 工作流自动化

**代码示例：**
- MetaGPT 软件公司
- Flask AI API
- ELiza 环境配置脚本
- N8N Docker 部署

**Prompt 汇编：**
- 文生图 Prompt（即梦AI、Gemini）
- 文生视频 Prompt（可灵、Sora）
- Vlog 生成 Prompt

---

## 使用指南

### 1. 查找特定章节的内容

```bash
# 进入第2章
cd chapter-2

# 查看 README
cat README.md

# 查看 Prompt 框架
ls prompts/frameworks/
```

### 2. 使用 Prompt

1. 找到对应的 `.md` 文件
2. 复制 Prompt 内容
3. 粘贴到大模型对话框
4. 根据需要调整参数

### 3. 运行代码

```bash
# 安装依赖
pip install -r requirements.txt

# 运行示例
python chapter-3/code/metagpt/software_company.py
```

---

## 文件统计

| 类型 | 数量 |
|------|------|
| Markdown 文件 | 22 |
| Python 文件 | 2 |
| Shell 脚本 | 1 |
| 总计 | 25 |

---

## 贡献指南

欢迎提交 Issue 和 Pull Request！

详见 [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 许可证

MIT License - 详见 [LICENSE](LICENSE)

---

**📖 返回目录** | **🚀 快速开始** | **📋 完整索引**
