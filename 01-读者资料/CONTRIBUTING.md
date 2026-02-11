# 贡献指南

感谢您对《动手做 AI Agent：零基础玩转智能体》配套代码仓库的关注！

---

## 🤝 如何贡献

### 报告问题

如果您发现任何问题：

1. 在 Issues 中搜索是否已有类似问题
2. 如果没有，创建新的 Issue，详细描述问题
3. 提供复现步骤和预期行为

### 提交代码

1. **Fork** 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

### 文件组织规范

本仓库按章节组织，新增内容请遵循以下结构：

```
chapter-X/           # X 为章节编号
├── README.md       # 章节介绍
├── prompts/         # Prompt 文件
├── code/            # 代码文件
├── guides/          # 指南文档
└── knowledge/       # 知识点总结
```

### 内容标注规范

所有新增文件必须包含来源标注：

```markdown
> **📍 来源**：第X章 X.X 节 [节标题]
> **📄 行号**：第 XXXX-XXXX 行
> **📖 页码**：第 XX 页
```

代码文件头部注释：

```python
"""
文件描述

来源：《动手做 AI Agent：零基础玩转智能体》
章节：第X章 X.X 节 [节标题]
行号：第 XXXX-XXXX 行
页码：第 XX 页
"""
```

---

## 📋 Pull Request 检查清单

提交 PR 前，请确认：

- [ ] 代码通过测试（如果有）
- [ ] 文档已更新
- [ ] 添加了来源标注
- [ ] 遵循文件组织规范
- [ ] Commit 信息清晰明确

---

## 📜 行为准则

- 尊重所有贡献者
- 欢迎不同观点和建设性讨论
- 专注于对社区最有利的事情

---

## 📧 联系方式

如有疑问，请通过以下方式联系：

- 提交 Issue
- 发送邮件至：author@example.com

感谢您的贡献！
