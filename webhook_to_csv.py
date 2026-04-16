import requests
import csv

ORG = "your-org"
REPO = "your-repo"
TOKEN = "ghp_xxx"

BASE = "https://api.github.com"

headers = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github+json"
}

def safe_get(url):
    try:
        r = requests.get(url, headers=headers, timeout=30)

        print(f"[DEBUG] {r.status_code} {url}")

        if r.status_code != 200:
            return None

        if not r.text.strip():
            return None

        return r.json()

    except Exception as e:
        print("[ERROR]", url, e)
        return None


def main():

    hooks_url = f"{BASE}/repos/{ORG}/{REPO}/hooks"
    hooks = safe_get(hooks_url)

    if not hooks:
        print("No hooks found or access denied")
        return

    filename = f"{ORG}_{REPO}_webhooks.csv"

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        # Header
        writer.writerow([
            "repo",
            "hook_id",
            "url",
            "active",
            "event_count",
            "last_delivery"
        ])

        for h in hooks:
            hook_id = h.get("id")
            url = h.get("config", {}).get("url", "N/A")
            active = h.get("active")

            deliveries_url = f"{hooks_url}/{hook_id}/deliveries"
            deliveries = safe_get(deliveries_url)

            if deliveries is None:
                event_count = 0
                last_delivery = "N/A"
            else:
                event_count = len(deliveries)
                last_delivery = deliveries[0]["delivered_at"] if event_count > 0 else "never"

            writer.writerow([
                f"{ORG}/{REPO}",
                hook_id,
                url,
                active,
                event_count,
                last_delivery
            ])

            print(f"Processed hook {hook_id}")

    print(f"\nCSV generated: {filename}")


if __name__ == "__main__":
    main()
