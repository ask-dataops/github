import sys
import requests
import csv

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

csv_file = "webhook_payload_urls.csv"

with open(csv_file, "a", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)

    for h in hooks:
        payload_url = h.get("config", {}).get("url")  # GitHub field

        writer.writerow([
            repo,
            payload_url
        ])

print(f"Processed {repo}")
