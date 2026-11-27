#!/usr/bin/env python3
"""Original reference harness for a local OpenAI-compatible endpoint.

This is a NEW harness, not the historical runner. No third-party question
banks, model responses, private URLs or tokens are written to disk.
Python 3.10+; standard library only.
"""
import argparse
import datetime as dt
import ipaddress
import json
import os
import sys
import time
import urllib.parse
import urllib.request

MARKERS = ("MKR-ALPHA-7361", "MKR-BETA-4829", "MKR-GAMMA-1957")


def build_prompt(records, task):
    if records < 3:
        raise ValueError("records must be at least 3")
    locations = {0: MARKERS[0], records // 2: MARKERS[1],
                 records - 1: MARKERS[2]}
    lines = []
    for i in range(records):
        line = (f"Record {i:06d}: module_{i % 97:02d} reviewed its "
                f"synthetic documentation; batch {i % 31:02d}, "
                f"checksum {i * 73 % 100003:06d}.")
        if i in locations:
            line += f" Unique reference: {locations[i]}."
        lines.append(line)
    question = ("Return the three unique reference markers exactly, in order."
                if task == "recall" else
                "Write a detailed numbered review of this synthetic engineering "
                "record collection, explaining data validation and documentation.")
    return "\n".join(lines) + "\n\n" + question


def local_url(base):
    p = urllib.parse.urlsplit(base)
    if p.scheme not in ("http", "https") or p.username or p.password or p.query or p.fragment:
        raise ValueError("Use a local HTTP(S) API base URL without credentials or query")
    host = p.hostname
    if host != "localhost":
        try:
            local = ipaddress.ip_address(host or "").is_loopback
        except ValueError:
            local = False
        if not local:
            raise ValueError("Only loopback endpoints are supported by this reference harness")
    return base.rstrip("/") + "/chat/completions"


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def sse_objects(lines):
    for raw in lines:
        line = raw.decode("utf-8").strip()
        if not line.startswith("data:"):
            continue
        payload = line[5:].strip()
        if payload == "[DONE]":
            return
        if payload:
            yield json.loads(payload)


def measure(args, prompt, sequence):
    request = {"model": args.model, "messages": [{"role": "user", "content": prompt}],
               "stream": True, "stream_options": {"include_usage": True},
               "temperature": 0, "max_tokens": args.max_tokens}
    headers = {"Content-Type": "application/json", "Accept": "text/event-stream"}
    key = os.environ.get("LOCAL_LLM_API_KEY")
    if key:
        headers["Authorization"] = "Bearer " + key
    req = urllib.request.Request(local_url(args.base_url),
        data=json.dumps(request).encode(), headers=headers, method="POST")
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), NoRedirect())
    start = time.perf_counter()
    first = first_visible = last = None
    usage = {}
    visible = []
    finish = None
    content_chars = reasoning_chars = 0
    with opener.open(req, timeout=args.timeout) as response:
        for obj in sse_objects(response):
            now = time.perf_counter()
            if isinstance(obj.get("usage"), dict):
                usage = obj["usage"]
            choices = obj.get("choices") or []
            if not choices:
                continue
            choice = choices[0]
            delta = choice.get("delta") or {}
            content = delta.get("content")
            reasoning = delta.get("reasoning_content") or delta.get("reasoning")
            content = content if isinstance(content, str) else ""
            reasoning = reasoning if isinstance(reasoning, str) else ""
            if content or reasoning:
                first = now if first is None else first
                last = now
            if content:
                first_visible = now if first_visible is None else first_visible
                content_chars += len(content)
                visible.append(content)
            reasoning_chars += len(reasoning)
            finish = choice.get("finish_reason") or finish
    end = time.perf_counter()
    completion = usage.get("completion_tokens")
    details = usage.get("prompt_tokens_details") or {}
    duration = last - first if first is not None and last is not None else None
    # Client estimate over observed streaming interval, not engine decode timing.
    estimate = completion / duration if (isinstance(completion, int) and
                    completion > 1 and duration and duration > 0) else None
    answer = "".join(visible)
    return {
        "timestamp_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "sequence": sequence,
        "cache_intent": "first_request" if sequence == 1 else "repeated_prompt",
        "task": args.task, "records": args.records, "model": args.model,
        "requested_max_tokens": args.max_tokens,
        "prompt_tokens": usage.get("prompt_tokens"),
        "cached_tokens": details.get("cached_tokens"),
        "completion_tokens": completion,
        "ttft_s": round(first - start, 6) if first is not None else None,
        "first_visible_s": round(first_visible - start, 6) if first_visible is not None else None,
        "wall_s": round(end - start, 6),
        "client_stream_toks_per_s_estimate": round(estimate, 3) if estimate is not None else None,
        "visible_chars": content_chars, "reasoning_chars": reasoning_chars,
        "markers_correct": sum(m in answer for m in MARKERS) if args.task == "recall" else None,
        "finish_reason": finish,
    }


def self_test():
    p = build_prompt(9, "recall")
    assert all(p.count(m) == 1 for m in MARKERS)
    assert local_url("http://127.0.0.1:1234/v1").endswith("/v1/chat/completions")
    for bad in ("https://example.com/v1", "http://localhost@evil.example/v1"):
        try:
            local_url(bad)
        except ValueError:
            pass
        else:
            raise AssertionError("non-local URL accepted")
    sample = [b"data: {\"choices\": []}\n", b"\n", b"data: [DONE]\n"]
    assert list(sse_objects(sample)) == [{"choices": []}]
    print("Offline self-test passed")


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--base-url", default="http://127.0.0.1:1234/v1")
    p.add_argument("--model")
    p.add_argument("--task", choices=("recall", "generation"), default="recall")
    p.add_argument("--records", type=int, default=100)
    p.add_argument("--max-tokens", type=int, default=256)
    p.add_argument("--repeat", type=int, default=2)
    p.add_argument("--timeout", type=float, default=300)
    p.add_argument("--out", default="benchmark-results.jsonl")
    p.add_argument("--self-test", action="store_true")
    a = p.parse_args()
    if a.self_test:
        self_test()
        return
    if not a.model or min(a.records, a.max_tokens, a.repeat, a.timeout) <= 0:
        p.error("provide --model and positive limits")
    prompt = build_prompt(a.records, a.task)
    for i in range(1, a.repeat + 1):
        try:
            result = measure(a, prompt, i)
        except Exception as exc:
            # No URL, request body, credentials or server response body in logs.
            result = {"sequence": i, "task": a.task, "records": a.records,
                      "error_type": type(exc).__name__,
                      "http_status": getattr(exc, "code", None)}
        line = json.dumps(result, ensure_ascii=False)
        with open(a.out, "a", encoding="utf-8") as output:
            output.write(line + "\n")
        print(line, flush=True)


if __name__ == "__main__":
    main()
