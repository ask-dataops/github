import sys
import requests
import csv
import json

ORG = "your-org"
TOKEN = "ghp_xxx"

repo = sys.argv[1]

url = f"https://api.github.com/repos/{ORG}/{repo}/hooks"

headers = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github+json"
}

resp = requests.get(url, headers=headers)
hooks = resp.json()

csv_file = "webhook_output.csv"

with open(csv_file, "a", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)

    for h in hooks:
        writer.writerow([
            repo,
            h.get("id"),
            h.get("active"),
            json.dumps(h)   # FULL PAYLOAD
        ])

print(f"Processed {repo}")
