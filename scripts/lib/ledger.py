"""绩效台账 - JSONL append-only ledger of past picks vs realized outcomes.

每一行：{
  "scan_date": "2026-04-30",      # 当日扫描
  "review_date": "2026-05-01",    # 复盘日
  "ticker": "$LITE",
  "direction": "long",
  "thesis_summary": "...",
  "entry_zone": "...",
  "stop": "...",
  "target": "...",
  "actual_change_pct": 2.3,       # 复盘日实际涨跌
  "verdict": "hit" | "miss" | "neutral",
  "layer_attribution": "Layer 2 — supply chain node mapping",
  "notes": "..."
}

蒸馏规则：连续 ≥3 次同一模式（同一 verdict、同一 layer、同一 sector）就提议候选规则。
"""

from __future__ import annotations
import json
from collections import Counter
from pathlib import Path
from typing import Iterator

LEDGER_DIR = (
    Path(__file__).resolve().parents[2]
    / "04-AI工具箱"
    / "提示词与工作流"
    / "瓶颈猎手-美股每日进化系统"
    / "08-知识沉淀"
)
LEDGER_PATH = LEDGER_DIR / "绩效台账.jsonl"


def append_entries(entries: list[dict]) -> int:
    LEDGER_DIR.mkdir(parents=True, exist_ok=True)
    with LEDGER_PATH.open("a", encoding="utf-8") as f:
        for e in entries:
            f.write(json.dumps(e, ensure_ascii=False) + "\n")
    return len(entries)


def read_all() -> list[dict]:
    if not LEDGER_PATH.exists():
        return []
    out: list[dict] = []
    with LEDGER_PATH.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return out


def recent_window(days: int = 30) -> list[dict]:
    """Return entries whose review_date is within the most recent N entries by date."""
    all_entries = read_all()
    # Simple cap by row count — fine for sub-1000 row ledger
    return all_entries[-days * 8 :] if len(all_entries) > days * 8 else all_entries


def emerging_patterns(min_count: int = 3) -> list[dict]:
    """Find patterns that have appeared ≥ min_count times. Each pattern = (verdict, layer)."""
    counter: Counter[tuple[str, str]] = Counter()
    samples: dict[tuple[str, str], list[dict]] = {}
    for e in read_all():
        key = (e.get("verdict", "?"), e.get("layer_attribution", "?"))
        counter[key] += 1
        samples.setdefault(key, []).append(e)
    out: list[dict] = []
    for (verdict, layer), count in counter.most_common():
        if count < min_count:
            continue
        out.append(
            {
                "verdict": verdict,
                "layer": layer,
                "count": count,
                "samples": samples[(verdict, layer)][:5],
            }
        )
    return out


def stats_summary() -> dict:
    entries = read_all()
    if not entries:
        return {"n": 0}
    n = len(entries)
    hits = sum(1 for e in entries if e.get("verdict") == "hit")
    misses = sum(1 for e in entries if e.get("verdict") == "miss")
    return {
        "n": n,
        "hits": hits,
        "misses": misses,
        "hit_rate": round(hits / n, 3) if n else 0.0,
    }
