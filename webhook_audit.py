import requests
import json
import sys

# ======================
# CONFIG
# ======================
ORG = "your-org"
REPO = "your-repo"
TOKEN = "ghp_xxx"

BASE = "https://api.github.com"

headers = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github+json"
}

# ======================
# SAFE API CALL
# ======================
def safe_get(url):
    try:
        r = requests.get(url, headers=headers, timeout=30)

        print(f"[DEBUG] {r.status_code} {url}")

        # Handle no content
        if r.status_code == 204:
            return []

        # Handle errors cleanly
        if r.status_code != 200:
            print(f"[SKIP] HTTP {r.status_code} -> {r.text[:200]}")
            return None

        # Empty response guard
        if not r.text or not r.text.strip():
            print("[SKIP] Empty response")
            return None

        # JSON parse safety
        try:
            return r.json()
        except Exception:
            print("[SKIP] Invalid JSON ->", r.text[:200])
            return None

    except Exception as e:
        print("[ERROR]", url, e)
        return None


# ======================
# GET HOOKS
# ======================
def get_hooks():
    url = f"{BASE}/repos/{ORG}/{REPO}/hooks"
    data = safe_get(url)

    if data is None:
        print("No hooks found or access blocked")
        sys.exit(1)

    if not isinstance(data, list):
        print("Unexpected response format (expected list)")
        sys.exit(1)

    return data


# ======================
# GET DELIVERIES
# ======================
def get_deliveries(hook_id):
    url = f"{BASE}/repos/{ORG}/{REPO}/hooks/{hook_id}/deliveries"
    data = safe_get(url)

    if data is None:
        return []

    if isinstance(data, list):
        return data

    return []


# ======================
# MAIN LOGIC
# ======================
def main():
    hooks = get_hooks()

    print(f"\nTotal hooks: {len(hooks)}\n")

    for h in hooks:
        hook_id = h.get("id")
        url = h.get("config", {}).get("url", "unknown")
        active = h.get("active")

        deliveries = get_deliveries(hook_id)

        if len(deliveries) == 0:
            print(f"❌ NEVER FIRED")
            print(f"   Repo: {ORG}/{REPO}")
            print(f"   Hook: {hook_id}")
            print(f"   URL : {url}")
            print(f"   Active: {active}")

            # OPTIONAL: disable hook (UNCOMMENT IF NEEDED)
            # disable_url = f"{BASE}/repos/{ORG}/{REPO}/hooks/{hook_id}"
            # safe_get(disable_url)

        else:
            print(f"✔ Used hook {hook_id} -> {len(deliveries)} deliveries")


if __name__ == "__main__":
    main()
