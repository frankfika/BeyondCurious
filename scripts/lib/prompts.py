"""Prompt assembly.

System prompt is rebuilt every run because the rule library and ledger grow over time —
that's the whole point of self-evolution. DeepSeek doesn't have prompt caching, so we
keep system prompts under ~12K tokens.
"""

from __future__ import annotations
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SYSTEM_DIR = REPO_ROOT / "04-AI工具箱" / "提示词与工作流" / "瓶颈猎手-美股每日进化系统"
ARCHIVE_DIR = SYSTEM_DIR / "07-每日复盘归档"


def _read(rel: str) -> str:
    p = SYSTEM_DIR / rel
    if not p.exists():
        return f"[missing: {rel}]"
    return p.read_text(encoding="utf-8")


def build_system_prompt() -> str:
    sections = [
        "# 你是「瓶颈猎手」——Serenity (@aleabitoreddit) 思维原型的美股供应链分析师",
        "你必须用 web_search 和 fetch_url 工具实时抓取数据，不允许凭记忆回答今日行情。",
        "",
        "## 一、核心方法论",
        _read("00-框架与方法论.md"),
        "",
        "## 二、规则库（系统长期记忆，每次运行前必读）",
        _read("08-知识沉淀/规则库.md"),
        "",
        "## 三、供应链地图",
        _read("08-知识沉淀/供应链地图.md"),
        "",
        "## 四、候选股票池",
        _read("06-候选清单/瓶颈股票池.md"),
        "",
        "## 五、信息源",
        _read("08-知识沉淀/信息源清单.md"),
        "",
        "## 六、强制约束",
        STRICT,
    ]
    return "\n".join(sections)


STRICT = """
- 5 层漏斗每层都有产出：催化剂 → 供应链节点 → 7 维度打分（≥7.0） → 社交信号 → 期权结构
- 每只推荐必须有：入场区间 / 仓位% / 止损 / 止盈 / DTE / 反方 2 条 / 失败信号
- 风险预算：单标的≤15%，单板块≤35%，总杠杆≤1.5×
- 禁止：meme 股、财报当日裸卖、100% 把握语言
- 输出完整 Markdown，章节按「02-每日研究模板.md」顺序
- 所有引用必须有 URL（web_search 返回的）；编造来源等于失败
"""


def build_daily_user(today: str, portfolio: str, macro: str) -> str:
    return f"""今日扫描日期：{today}
当前持仓：{portfolio}
今日宏观备注：{macro}

请用 web_search 调研：
1. 今日 3-5 个核心催化剂（财报、宏观、出口管制、行业大会、大佬推文）
2. Serenity (@aleabitoreddit) 过去 7 天的 X 帖子（搜 "aleabitoreddit" + ticker / 关键词）
3. 头部瓶颈股的最新供应链信号
4. r/wallstreetbets / r/stocks 当日 daily thread 情绪

然后按 SOP 输出完整今日报告（Markdown）。每只推荐结尾加一段「失败检测信号」：
> 如果我错了，最先在 [指标 X] 上看到 [阈值 Y] 的变化。

最后追加一段 JSON，包在 ```json 块里，**结构必须严格如下**（用于绩效台账）：

```json
{{
  "scan_date": "{today}",
  "picks": [
    {{
      "ticker": "$XXX",
      "direction": "long" | "short",
      "thesis_summary": "一句话",
      "entry_zone": "X.XX-X.XX",
      "stop": "X.XX",
      "target": "X.XX",
      "structure": "正股 / SellPut30Δ / ...",
      "primary_layer": "Layer 1 catalysts | Layer 2 supply chain | Layer 3 scorecard | Layer 4 social | Layer 5 options"
    }}
  ]
}}
```
"""


def build_review_user(yesterday_md: str, picks_json: list[dict], today: str) -> str:
    picks_table = "\n".join(
        f"- {p.get('ticker')} {p.get('direction')} entry={p.get('entry_zone')} stop={p.get('stop')} target={p.get('target')} layer={p.get('primary_layer')}"
        for p in picks_json
    )
    return f"""任务：复盘 {yesterday_md} 报告中的推荐，今日是 {today}。

待复盘标的：
{picks_table}

请用 web_search 查每只标的从上次扫描至今的实际表现（百分比变化、是否触发止损/止盈/反方信号）。

然后输出 JSON，包在 ```json 块里，**结构必须严格如下**（将写入绩效台账 jsonl）：

```json
{{
  "review_date": "{today}",
  "entries": [
    {{
      "scan_date": "{yesterday_md.replace('.md','')}",
      "review_date": "{today}",
      "ticker": "$XXX",
      "direction": "long" | "short",
      "thesis_summary": "原论点",
      "entry_zone": "X.XX-X.XX",
      "stop": "X.XX",
      "target": "X.XX",
      "actual_change_pct": 0.0,
      "verdict": "hit" | "miss" | "neutral",
      "layer_attribution": "...",
      "notes": "为什么对/错"
    }}
  ]
}}
```
不要其他评论，只输出 JSON。
"""


def build_distill_user(patterns: list[dict], current_rules: str) -> str:
    return f"""任务：从绩效台账涌现的模式中蒸馏候选规则。

涌现模式（已出现 ≥3 次）：
```json
{patterns}
```

现有规则库内容（节选「候选区」）：
```
{current_rules[:3000]}
```

为每个新模式提出 1 条候选规则，格式严格如下（直接 append 到规则库候选区）：

```markdown
### [候选] 反规则 · 提出日 YYYY-MM-DD
- 触发条件：（来自模式的 layer + verdict）
- 应执行动作：（具体可执行）
- 已观察次数：{{count}} / 3
- 关联台账：（前 3 个样本的 scan_date）
```

不要修改已有规则，只输出新增的 markdown 段落。
"""


def build_critic_user(today_report: str) -> str:
    return f"""任务：审计今日扫描报告。你是「红队」，目标是找它的漏洞。

请按以下顺序检查：
1. **数据来源**：每个核心论点是否有 URL？是否有看起来像编造的引用？
2. **规则触犯**：对照规则库正式规则 + 反规则，逐条检查每只推荐
3. **盲点**：今日有哪些催化剂被忽略了？哪些板块没看？
4. **风险预算**：仓位是否突破单标的 15% / 单板块 35%？
5. **反方完整性**：每只推荐的反方论点是否真的能证伪，还是稻草人？
6. **失败信号**：「如果错了在哪里看到」是否可观察 + 可量化？

如果发现严重问题（漏洞≥1 或触犯反规则），在批注开头加：
🚨 **CRITICAL ISSUES FOUND**

输出 Markdown 段落，以 `## 自审批注（红队复核）` 为标题。

待审报告：
---
{today_report[:20000]}
"""
