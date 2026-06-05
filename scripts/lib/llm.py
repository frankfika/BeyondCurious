"""DeepSeek wrapper via OpenAI-compatible SDK.

Implements the agentic tool-calling loop manually:
- send messages → if response has tool_calls, execute them, append results, repeat
- terminate when no tool_calls (final answer) or max iters reached
"""

from __future__ import annotations
import json
import os
import sys
from typing import Any, Iterable

from openai import OpenAI

from . import fetcher

DEEPSEEK_BASE_URL = "https://api.deepseek.com/v1"
DEFAULT_MODEL = os.environ.get("DEEPSEEK_MODEL", "deepseek-chat")
DEFAULT_CRITIC_MODEL = os.environ.get("DEEPSEEK_MODEL_CRITIC", "deepseek-reasoner")
MAX_ITERS = int(os.environ.get("TOOL_LOOP_MAX_ITERS", "12"))


def _client() -> OpenAI:
    key = os.environ.get("DEEPSEEK_API_KEY")
    if not key:
        raise RuntimeError("DEEPSEEK_API_KEY not set")
    return OpenAI(api_key=key, base_url=DEEPSEEK_BASE_URL)


def run_agent(
    system_prompt: str,
    user_message: str,
    *,
    model: str = DEFAULT_MODEL,
    with_tools: bool = True,
    max_iters: int = MAX_ITERS,
    log_to_stderr: bool = True,
) -> tuple[str, dict]:
    """Run an agentic loop. Returns (final_text, usage_dict).

    DeepSeek-chat supports OpenAI-style tool_calls. We loop:
        model emits tool_calls → we execute → append tool messages → call again
    until the model returns a normal `content` answer (no tool_calls).
    """
    client = _client()

    messages: list[dict[str, Any]] = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message},
    ]

    tools = fetcher.TOOL_SCHEMAS if with_tools else None
    usage_total = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}

    for iteration in range(max_iters):
        if log_to_stderr:
            print(f"[llm] iter {iteration+1}/{max_iters}", file=sys.stderr)

        kwargs: dict[str, Any] = {
            "model": model,
            "messages": messages,
            "max_tokens": 8192,
        }
        if tools:
            kwargs["tools"] = tools
            kwargs["tool_choice"] = "auto"

        resp = client.chat.completions.create(**kwargs)

        if resp.usage:
            usage_total["prompt_tokens"] += resp.usage.prompt_tokens or 0
            usage_total["completion_tokens"] += resp.usage.completion_tokens or 0
            usage_total["total_tokens"] += resp.usage.total_tokens or 0

        choice = resp.choices[0]
        msg = choice.message

        # Append assistant message verbatim
        assistant_entry: dict[str, Any] = {
            "role": "assistant",
            "content": msg.content or "",
        }
        if msg.tool_calls:
            assistant_entry["tool_calls"] = [
                {
                    "id": tc.id,
                    "type": "function",
                    "function": {
                        "name": tc.function.name,
                        "arguments": tc.function.arguments,
                    },
                }
                for tc in msg.tool_calls
            ]
        messages.append(assistant_entry)

        if not msg.tool_calls:
            # Final answer
            usage_total["iterations"] = iteration + 1
            usage_total["model"] = model
            usage_total["stop_reason"] = choice.finish_reason
            return msg.content or "", usage_total

        # Execute each tool call
        for tc in msg.tool_calls:
            name = tc.function.name
            try:
                args = json.loads(tc.function.arguments or "{}")
            except json.JSONDecodeError:
                args = {}
            if log_to_stderr:
                print(f"[llm]   tool: {name}({list(args.keys())})", file=sys.stderr)
            result = fetcher.execute_tool(name, args)
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tc.id,
                    "content": json.dumps(result, ensure_ascii=False, default=str)[
                        :12000
                    ],
                }
            )

    # Hit iteration limit
    usage_total["iterations"] = max_iters
    usage_total["model"] = model
    usage_total["stop_reason"] = "max_iters"
    last_text = (messages[-1].get("content") or "") if messages else ""
    return last_text, usage_total


def run_simple(
    system_prompt: str,
    user_message: str,
    *,
    model: str = DEFAULT_CRITIC_MODEL,
) -> tuple[str, dict]:
    """One-shot call without tools (used for critic / distillation steps)."""
    client = _client()
    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
        max_tokens=8192,
    )
    usage = {
        "prompt_tokens": resp.usage.prompt_tokens if resp.usage else 0,
        "completion_tokens": resp.usage.completion_tokens if resp.usage else 0,
        "total_tokens": resp.usage.total_tokens if resp.usage else 0,
        "model": model,
        "stop_reason": resp.choices[0].finish_reason,
    }
    return resp.choices[0].message.content or "", usage
