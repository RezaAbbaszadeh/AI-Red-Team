#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
import urllib.error
import urllib.request

BASE_URL = "http://127.0.0.1:5000"


def request_json(path: str, method: str = "GET", body: dict | None = None) -> dict:
    data = None
    headers = {}
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        headers["Content-Type"] = "application/json"

    request = urllib.request.Request(
        f"{BASE_URL}{path}",
        data=data,
        headers=headers,
        method=method,
    )

    with urllib.request.urlopen(request, timeout=180) as response:
        payload = response.read().decode("utf-8")
        return json.loads(payload)


def main() -> int:
    try:
        health = request_json("/api/health")
        print("[PASS] Health:", health)

        models = request_json("/api/models")
        print("[PASS] Agent model:", models.get("agentic_model"))

        result = request_json(
            "/api/agent/chat",
            method="POST",
            body={
                "prompt": "List the users available in this synthetic lab.",
                "tool_names": ["list_users"],
                "max_steps": 5,
                "timeout": 120,
            },
        )

        if "response" not in result or "tool_calls" not in result:
            print("[FAIL] Agent response is missing expected fields.")
            print(json.dumps(result, indent=2))
            return 1

        print("[PASS] Agent response received.")
        print("[INFO] Tool calls:", result.get("tool_calls"))
        print("[INFO] Response preview:", str(result.get("response", ""))[:300])

        if "list_users" not in result.get("tool_calls", []):
            print("[WARN] The model did not call list_users. Retry once before debugging.")
        return 0

    except urllib.error.URLError as exc:
        print(f"[FAIL] Could not reach DVAIA at {BASE_URL}: {exc}")
        return 1
    except Exception as exc:
        print(f"[FAIL] Verification error: {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
