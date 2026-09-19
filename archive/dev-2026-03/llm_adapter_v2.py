#!/usr/bin/env python3
# ==============================================================================
# NORE Universal LLM Adapter
# ==============================================================================
# Supports both Together AI and OpenAI backends via a unified interface.
# Auto-detects backend from model name, or accepts explicit override.
#
# Usage:
#   from llm_adapter import llm_chat_universal, detect_backend
#   response = llm_chat_universal(model="gpt-4.1-mini", messages=[...])
# ==============================================================================

import os
import json
import logging
from typing import Optional

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv optional — env vars can be set directly

log = logging.getLogger("llm_adapter")

# ---------------------------------------------------------------------------
# Backend detection
# ---------------------------------------------------------------------------

OPENAI_PREFIXES = ("gpt-", "o1", "o3", "o4", "o5", "chatgpt-", "ft:gpt-")


def detect_backend(model: str) -> str:
    """Auto-detect 'openai' or 'together' from model name."""
    model_lower = model.lower().strip()
    for prefix in OPENAI_PREFIXES:
        if model_lower.startswith(prefix):
            return "openai"
    if "/" in model:
        return "together"
    if os.getenv("OPENAI_API_KEY") and not os.getenv("TOGETHER_API_KEY"):
        return "openai"
    return "together"


# ---------------------------------------------------------------------------
# Together AI
# ---------------------------------------------------------------------------

_together_client = None

def _get_together_client():
    global _together_client
    if _together_client is None:
        from together import Together
        _together_client = Together(api_key=os.getenv("TOGETHER_API_KEY"))
    return _together_client


def llm_chat_together(model, messages, temperature=0.2, max_tokens=1024, top_p=0.9):
    client = _get_together_client()
    resp = client.chat.completions.create(
        model=model, messages=messages,
        temperature=temperature, max_tokens=max_tokens, top_p=top_p,
    )
    return (resp.choices[0].message.content or "").strip()


# ---------------------------------------------------------------------------
# OpenAI
# ---------------------------------------------------------------------------

_openai_client = None

def _get_openai_client():
    global _openai_client
    if _openai_client is None:
        from openai import OpenAI
        _openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    return _openai_client


def llm_chat_openai(model, messages, temperature=0.2, max_tokens=1024, top_p=0.9):
    client = _get_openai_client()
    resp = client.chat.completions.create(
        model=model, messages=messages,
        temperature=temperature, max_tokens=max_tokens, top_p=top_p,
    )
    return (resp.choices[0].message.content or "").strip()


# ---------------------------------------------------------------------------
# Universal dispatcher
# ---------------------------------------------------------------------------

_call_counter = 0

def llm_chat_universal(model, messages, temperature=0.2, max_tokens=1024,
                       top_p=0.9, backend=None):
    """
    Route to the correct backend based on model name or explicit override.
    
    Returns the assistant's response text (stripped).
    """
    global _call_counter
    _call_counter += 1

    if backend is None:
        backend = detect_backend(model)

    log.debug(f"LLM call #{_call_counter}: {backend}/{model} ({len(messages)} msgs)")

    if backend == "openai":
        return llm_chat_openai(model, messages, temperature, max_tokens, top_p)
    elif backend == "together":
        return llm_chat_together(model, messages, temperature, max_tokens, top_p)
    else:
        raise ValueError(f"Unknown backend: {backend}")


# ---------------------------------------------------------------------------
# Legacy wrappers
# ---------------------------------------------------------------------------

def _extract_json_block(text):
    start, end = text.find("{"), text.rfind("}")
    if start == -1 or end == -1 or end <= start:
        raise ValueError("Could not locate JSON object in response.")
    return text[start:end + 1]


def llm_chat(messages, model=None, max_tokens=2000, temperature=0.0):
    """Legacy wrapper for PTPC triage. Returns strict JSON string."""
    model = model or os.getenv("TOGETHER_MODEL") or "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo"
    content = llm_chat_universal(model=model, messages=messages,
                                 temperature=temperature, max_tokens=max_tokens,
                                 backend="together")
    try:
        json.loads(content)
        return content
    except Exception:
        cleaned = _extract_json_block(content)
        json.loads(cleaned)
        return cleaned


def llm_smoke_test(model=None, backend=None):
    """Quick connectivity check."""
    model = model or os.getenv("TOGETHER_MODEL") or "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo"
    if backend is None:
        backend = detect_backend(model)
    print(f"Smoke test: {backend}/{model}")
    try:
        resp = llm_chat_universal(
            model=model,
            messages=[
                {"role": "system", "content": "You are a precise scientific assistant."},
                {"role": "user", "content": "Reply with exactly: OK"},
            ],
            temperature=0.0, max_tokens=8, backend=backend,
        )
        print(f"  Response: {resp}")
        return True
    except Exception as e:
        print(f"  FAILED: {e}")
        return False


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description="NORE LLM Adapter — smoke test")
    ap.add_argument("--model", default=None)
    ap.add_argument("--backend", choices=["openai", "together"], default=None)
    args = ap.parse_args()

    print("=" * 60)
    print("NORE LLM Adapter — Environment Check")
    print("=" * 60)
    print(f"  TOGETHER_API_KEY: {'set' if os.getenv('TOGETHER_API_KEY') else 'NOT SET'}")
    print(f"  OPENAI_API_KEY:   {'set' if os.getenv('OPENAI_API_KEY') else 'NOT SET'}")
    print()

    test_models = ["gpt-4.1", "gpt-4.1-mini", "moonshotai/Kimi-K2-Instruct-0905"]
    print("Backend auto-detection:")
    for m in test_models:
        print(f"  {m:50s} -> {detect_backend(m)}")
    print()

    llm_smoke_test(model=args.model, backend=args.backend)
