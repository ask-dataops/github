import requests

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

        print(f"[GET] {r.status_code} {url}")

        if r.status_code == 204:
            return []

        if r.status_code != 200:
            print(f"[SKIP GET] {r.status_code} {r.text[:200]}")
            return None

        if not r.text.strip():
            return None

        return r.json()

    except Exception as e:
        print("[ERROR GET]", url, e)
        return None


def disable_hook(hook_id):
    url = f"{BASE}/repos/{ORG}/{REPO}/hooks/{hook_id}"

    try:
        r = requests.patch(
            url,
            headers=headers,
            json={"active": False},
            timeout=30
        )

        print(f"[PATCH] {r.status_code} Disable hook {hook_id}")

        if r.status_code not in [200, 202]:
            print("[FAILED]", r.text[:200])

    except Exception as e:
        print("[ERROR PATCH]", hook_id, e)


def main():

    hooks_url = f"{BASE}/repos/{ORG}/{REPO}/hooks"
    hooks = safe_get(hooks_url)

    if not hooks:
        print("No hooks found")
        return

    disabled_count = 0

    for h in hooks:
        hook_id = h.get("id")
        active = h.get("active", False)
        url = h.get("config", {}).get("url", "N/A")

        if not active:
            print(f"[SKIP] Already inactive hook {hook_id}")
            continue

        deliveries_url = f"{hooks_url}/{hook_id}/deliveries"
        deliveries = safe_get(deliveries_url)

        if deliveries is None:
            print(f"[SKIP] Could not fetch deliveries for {hook_id}")
            continue

        if len(deliveries) == 0:
            print(f"[DISABLE] Never fired hook {hook_id} -> {url}")
            disable_hook(hook_id)
            disabled_count += 1
        else:
            print(f"[KEEP] Hook {hook_id} has {len(deliveries)} deliveries")

    print(f"\nDone. Disabled {disabled_count} hooks.")


if __name__ == "__main__":
    main()
