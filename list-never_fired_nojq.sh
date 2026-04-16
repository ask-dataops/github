#!/bin/bash

ORG="your-org"
TOKEN="ghp_xxx"
API="https://api.github.com"

echo "Listing NEVER-FIRED webhooks (ABC anywhere, case-insensitive)..."

curl -s -H "Authorization: token $TOKEN" \
"$API/orgs/$ORG/repos?per_page=100" | python3 - <<'PY'

import sys, json, subprocess

data = json.load(sys.stdin)

for repo in data:
    name = repo["name"]

    if "abc" not in name.lower():
        continue

    print(f"\n=== Repo: {name} ===")

    hooks = subprocess.check_output([
        "curl","-s","-H",f"Authorization: token {TOKEN}",
        f"{API}/repos/{ORG}/{name}/hooks"
    ])

    hooks = json.loads(hooks)

    for h in hooks:
        hid = h["id"]
        url = h["config"].get("url","")

        deliveries = subprocess.check_output([
            "curl","-s","-H",f"Authorization: token {TOKEN}",
            f"{API}/repos/{ORG}/{name}/hooks/{hid}/deliveries"
        ])

        deliveries = json.loads(deliveries)

        if len(deliveries) == 0:
            print(f"NEVER FIRED -> {hid} -> {url}")
PY
