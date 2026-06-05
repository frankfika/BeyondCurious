# 瓶颈猎手 · 美股每日自进化系统

> 思维原型：Serenity（@aleabitoreddit on X，原 Reddit WSB）——AI / 半导体供应链分析师，主张「逆向拆解供应链 → 锁定无人关注的瓶颈点 → 在机构轮动前建仓」，并以期权卖方策略择时放大收益。

## 这套系统是干什么的

每天用一套**固定 SOP** 让 AI（Claude / GPT / Gemini 任意一个）：

1. **扫描** 当日美股盘前 / 盘中 / 盘后的催化剂、社交情绪、供应链信号；
2. **复用 Serenity 的思维链** 进行二阶 / 三阶推理（不是看 K 线，是看产业链位置）；
3. **筛出 3–5 只今日值得行动的票**，给出仓位、入场区间、止损、退出条件；
4. **晚间复盘**，把当日命中 / 未命中的归因写入「知识沉淀」，下次自动调用——这就是「自进化」。

## 目录

| 文件 | 用途 |
|---|---|
| `00-框架与方法论.md` | Serenity 思维原型 + 我们落地的 5 层筛选漏斗 |
| `01-每日工作流SOP.md` | 盘前 / 盘中 / 盘后三段式时间表，每段做什么 |
| `02-每日研究模板.md` | Copy-paste 用的当日研究 Markdown 模板 |
| `03-持仓与交易日志.md` | 真实持仓 + 每笔交易的入场 / 出场理由 |
| `04-自进化复盘机制.md` | 周复盘 / 月复盘，把战胜 & 败因蒸馏成规则 |
| `05-Claude执行提示词.md` | 直接喂给 Claude / GPT 的 system prompt，可一键运行 |
| `06-候选清单/` | 当前监控的瓶颈股票池（按板块） |
| `07-每日复盘归档/` | 每天一个文件，命名 `YYYY-MM-DD.md` |
| `08-知识沉淀/` | 经过复盘验证的可复用规则 / 反规则 |

## 快速开始 · 完全自动化 + 自进化循环

每次 GitHub Actions cron 自动跑**4 阶段循环**——这就是「自进化」：

```
Phase A · 复盘昨日 → 给昨日推荐打分 → 写入 08-知识沉淀/绩效台账.jsonl
Phase B · 蒸馏规则 → 扫台账，连续 ≥3 次模式 → 写入规则库候选区
Phase C · 今日扫描 → 用最新规则库 + 工具循环 → 出今日报告
Phase D · 自审（红队）→ 第二个 LLM 检查今日报告漏洞 → 追加批注
```

### 配置（一次性，5 分钟）

1. GitHub repo Settings → Secrets and variables → Actions → **New repository secret**
   - 名字：`DEEPSEEK_API_KEY`
   - 值：从 https://platform.deepseek.com/api_keys 拿
2. 可选 Variables：`DEEPSEEK_MODEL=deepseek-chat`（默认）、`DEEPSEEK_MODEL_CRITIC=deepseek-reasoner`（自审用更强模型）
3. Actions 标签页 → `瓶颈猎手 · 每日自进化循环` → `Run workflow` 触发首次
4. 之后工作日盘前 07:30 ET 自动跑

### 本地跑

```bash
pip install -r scripts/requirements.txt
export DEEPSEEK_API_KEY=sk-...

python scripts/run_scan.py loop                    # 完整 4 阶段（推荐）
python scripts/run_scan.py daily                   # 只 Phase C
python scripts/run_scan.py review                  # 只 Phase A+B
python scripts/run_scan.py critic --file 2026-04-30.md  # 只 Phase D
```

## 自动化架构

```
GitHub Actions cron (工作日 07:30 ET)
        ↓
scripts/run_scan.py loop
        ↓
┌─ A 复盘 ──→ DeepSeek-chat + web_search 查昨日实际涨跌 → 绩效台账.jsonl
├─ B 蒸馏 ──→ DeepSeek-chat 扫台账 + 现有规则 → 规则库候选区
├─ C 扫描 ──→ DeepSeek-chat + 工具循环（DuckDuckGo + fetch_url）
│              ├─ 5 层漏斗 → 出今日报告 Markdown
│              └─ 结尾输出 picks JSON（下次 A 阶段会用）
└─ D 自审 ──→ DeepSeek-reasoner 红队复核 → 追加自审批注

→ git commit + push（自动回本分支）
```

**成本估算**（DeepSeek-chat 输入 $0.27/M、输出 $1.10/M）：
- 每次完整循环 ≈ **$0.05-0.20**
- 月度总成本 ≈ **$1-5**（每月 ~22 个交易日）

DeepSeek 没有 Claude 那种内置 web_search，所以系统自带 DuckDuckGo + fetch_url 函数工具——免 key、免限速。如果 DuckDuckGo 被墙了，换 Tavily / Brave / SerpAPI 都只需改 `lib/fetcher.py` 一个文件。

## ⚠️ 风险声明

本系统是**研究框架与决策辅助工具**，不是投资建议。期权卖方策略尤其需要先具备：择时能力、组合保证金账户、严格止损纪律。亏钱不要找 AI 算账。
