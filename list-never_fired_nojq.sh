#!/bin/bash

ORG="your-org"
REPO="your-repo"
TOKEN="ghp_xxx"

API="https://api.github.com"

echo "Checking repo: $ORG/$REPO"

hooks=$(curl -s -H "Authorization: token $TOKEN" \
"$API/repos/$ORG/$REPO/hooks")

echo "$hooks" | python3 - <<'PY'
import json, subprocess

import sys

hooks = json.load(sys.stdin)

ORG="your-org"
REPO="your-repo"
TOKEN="ghp_xxx"
API="https://api.github.com"

for h in hooks:
    hid = h["id"]
    url = h["config"].get("url","")

    cmd = [
        "curl","-s","-H",f"Authorization: token {TOKEN}",
        f"{API}/repos/{ORG}/{REPO}/hooks/{hid}/deliveries"
    ]

    deliveries = json.loads(subprocess.check_output(cmd))

    if len(deliveries) == 0:
        print(f"NEVER FIRED -> {hid} -> {url}")
PY
