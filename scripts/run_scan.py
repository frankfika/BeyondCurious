#!/usr/bin/env python3
"""瓶颈猎手 - 4 阶段自进化循环.

每次运行（每日 GitHub Action cron）：
  Phase A · 复盘昨日 → 给昨日推荐打分 → 写入 08-知识沉淀/绩效台账.jsonl
  Phase B · 蒸馏规则 → 扫台账，连续 ≥3 次模式 → 写入规则库候选区
  Phase C · 今日扫描 → 用最新规则库 + 工具循环 → 出今日报告
  Phase D · 自审 → 第二轮 LLM 检查今日报告 → 追加批注

CLI:
    python scripts/run_scan.py loop              # 完整 4 阶段循环（GH Actions 默认）
    python scripts/run_scan.py daily             # 只跑 C
    python scripts/run_scan.py review            # 只跑 A+B
    python scripts/run_scan.py critic --file X.md  # 只跑 D
"""

from __future__ import annotations
import argparse
import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib import archiver, ledger, llm, prompts  # noqa: E402


def _today() -> str:
    return datetime.utcnow().date().isoformat()


# ---------- Phase A: review yesterday ----------


def phase_a_review() -> dict:
    """Pull yesterday's report, ask LLM to fetch actual prices and score each pick."""
    found = archiver.find_yesterday_report()
    if not found:
        print("[A] no prior report, skipping review", file=sys.stderr)
        return {"skipped": True, "reason": "no_prior_report"}

    last_path, last_text = found
    yesterday_name = last_path.name
    print(f"[A] reviewing {yesterday_name}", file=sys.stderr)

    picks_block = archiver.extract_json(last_text)
    if not picks_block or "picks" not in picks_block:
        print("[A] no picks JSON in yesterday's report", file=sys.stderr)
        return {"skipped": True, "reason": "no_picks_json"}

    system = prompts.build_system_prompt()
    user = prompts.build_review_user(
        yesterday_md=yesterday_name,
        picks_json=picks_block["picks"],
        today=_today(),
    )
    text, usage = llm.run_agent(system, user)
    review_json = archiver.extract_json(text)
    if not review_json or "entries" not in review_json:
        print("[A] couldn't parse review JSON", file=sys.stderr)
        return {"skipped": True, "reason": "parse_failed", "usage": usage}

    n = ledger.append_entries(review_json["entries"])
    print(f"[A] appended {n} entries to ledger", file=sys.stderr)
    return {"ok": True, "entries": n, "usage": usage}


# ---------- Phase B: distill rules ----------


def phase_b_distill() -> dict:
    patterns = ledger.emerging_patterns(min_count=3)
    if not patterns:
        print("[B] no emerging patterns ≥3, skipping", file=sys.stderr)
        return {"skipped": True}

    print(f"[B] {len(patterns)} emerging patterns", file=sys.stderr)
    rules_text = archiver.RULES_PATH.read_text(encoding="utf-8") if archiver.RULES_PATH.exists() else ""
    system = "你是规则蒸馏助手。基于已观察的模式产出可执行规则草案。"
    user = prompts.build_distill_user(patterns, rules_text)
    text, usage = llm.run_simple(system, user, model=llm.DEFAULT_MODEL)
    archiver.append_rules(text)
    print("[B] appended candidate rules", file=sys.stderr)
    return {"ok": True, "patterns": len(patterns), "usage": usage}


# ---------- Phase C: today's scan ----------


def phase_c_scan() -> tuple[str, list[dict], Path]:
    today = _today()
    portfolio = os.environ.get("PORTFOLIO", "（未提供）")
    macro = os.environ.get("MACRO_NOTE", "（待 web_search 抓取）")

    system = prompts.build_system_prompt()
    user = prompts.build_daily_user(today, portfolio, macro)

    print(f"[C] scanning for {today}", file=sys.stderr)
    text, usage = llm.run_agent(system, user)
    target = archiver.archive_report(f"{today}.md", text, usage)
    print(f"[C] wrote {target.name}", file=sys.stderr)
    return text, [usage], target


# ---------- Phase D: critique ----------


def phase_d_critic(report_text: str, target_path: Path) -> dict:
    print("[D] running critic", file=sys.stderr)
    system = "你是红队审计师。你的目标不是认可而是找漏洞。"
    user = prompts.build_critic_user(report_text)
    critic_text, usage = llm.run_simple(system, user)

    # Append critique to the report
    existing = target_path.read_text(encoding="utf-8")
    # Insert critique BEFORE the auto-generated footer
    if "<sub>自动生成" in existing:
        head, footer = existing.split("---\n\n<sub>自动生成", 1)
        new_text = head.rstrip() + "\n\n" + critic_text.strip() + "\n\n---\n\n<sub>自动生成" + footer
    else:
        new_text = existing.rstrip() + "\n\n" + critic_text.strip() + "\n"
    target_path.write_text(new_text, encoding="utf-8")
    print("[D] critique appended", file=sys.stderr)
    return {"ok": True, "usage": usage}


# ---------- commands ----------


def cmd_loop(_args) -> int:
    summary = {"date": _today(), "phases": {}}
    summary["phases"]["A"] = phase_a_review()
    summary["phases"]["B"] = phase_b_distill()
    report_text, usages, target = phase_c_scan()
    summary["phases"]["C"] = {"ok": True, "path": str(target.name)}
    summary["phases"]["D"] = phase_d_critic(report_text, target)
    summary["ledger_stats"] = ledger.stats_summary()
    print(json.dumps(summary, ensure_ascii=False, indent=2, default=str), file=sys.stderr)
    return 0


def cmd_daily(_args) -> int:
    phase_c_scan()
    return 0


def cmd_review(_args) -> int:
    phase_a_review()
    phase_b_distill()
    return 0


def cmd_critic(args) -> int:
    target = archiver.ARCHIVE_DIR / args.file
    if not target.exists():
        print(f"file not found: {target}", file=sys.stderr)
        return 1
    phase_d_critic(target.read_text(encoding="utf-8"), target)
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("loop", help="完整 4 阶段自进化循环（推荐）")
    sub.add_parser("daily", help="只跑 Phase C（今日扫描）")
    sub.add_parser("review", help="只跑 Phase A+B（复盘 + 蒸馏）")
    cr = sub.add_parser("critic", help="只跑 Phase D（红队审计指定报告）")
    cr.add_argument("--file", required=True, help="YYYY-MM-DD.md")

    args = parser.parse_args()
    handlers = {
        "loop": cmd_loop,
        "daily": cmd_daily,
        "review": cmd_review,
        "critic": cmd_critic,
    }
    return handlers[args.cmd](args)


if __name__ == "__main__":
    raise SystemExit(main())
