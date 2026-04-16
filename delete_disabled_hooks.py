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
            print(f"[SKIP] {r.status_code} {r.text[:200]}")
            return None

        if not r.text.strip():
            return None

        return r.json()

    except Exception as e:
        print("[ERROR GET]", url, e)
        return None


def delete_hook(hook_id):
    url = f"{BASE}/repos/{ORG}/{REPO}/hooks/{hook_id}"

    try:
        r = requests.delete(url, headers=headers, timeout=30)

        print(f"[DELETE] {r.status_code} Hook {hook_id}")

        if r.status_code not in [204, 200]:
            print("[FAILED DELETE]", r.text[:200])

    except Exception as e:
        print("[ERROR DELETE]", hook_id, e)


def main():

    hooks_url = f"{BASE}/repos/{ORG}/{REPO}/hooks"
    hooks = safe_get(hooks_url)

    if not hooks:
        print("No hooks found")
        return

    deleted = 0

    for h in hooks:
        hook_id = h.get("id")
        active = h.get("active", True)
        url = h.get("config", {}).get("url", "N/A")

        if active:
            print(f"[KEEP] Active hook {hook_id} -> {url}")
            continue

        print(f"[DELETE] Disabled hook {hook_id} -> {url}")
        delete_hook(hook_id)
        deleted += 1

    print(f"\nDone. Deleted {deleted} disabled hooks.")


if __name__ == "__main__":
    main()
