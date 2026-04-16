import requests
import csv
import sys
import subprocess

ORG = "your-org"
TOKEN = "ghp_xxx"

BASE = "https://api.github.com"

headers = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github+json"
}

def get_page(page):
    url = f"{BASE}/orgs/{ORG}/repos?per_page=100&page={page}"
    r = requests.get(url, headers=headers, timeout=30)

    print(f"[GET] {r.status_code} page={page}")

    if r.status_code != 200:
        print(r.text[:200])
        return None

    return r.json()


def main():

    if len(sys.argv) < 2:
        print("Usage: python export_repos.py <filter_text>")
        sys.exit(1)

    filter_text = sys.argv[1].lower()

    filename = f"{filter_text}_repos.csv"

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        writer.writerow([
            "repo_name",
            "full_name",
            "private",
            "url",
            "created_at",
            "updated_at",
            "default_branch"
        ])

        page = 1
        count = 0

        while True:
            repos = get_page(page)

            if not repos:
                break

            if len(repos) == 0:
                break

            for repo in repos:
                name = repo.get("name", "")

                # 🔥 dynamic filter (abc, ABC, service, etc.)
                if filter_text not in name.lower():
                    continue

                writer.writerow([
                    repo.get("name"),
                    repo.get("full_name"),
                    repo.get("private"),
                    repo.get("html_url"),
                    repo.get("created_at"),
                    repo.get("updated_at"),
                    repo.get("default_branch"),
                ])

                count += 1
                print(f"[MATCH] {name}")
                subprocess.run([
                    "python",
                    "webhook_to_csv_v2.py",
                    repo.get("name")
               ])


            page += 1

    print(f"\nDone. Total matched repos: {count}")
    print(f"CSV saved: {filename}")


if __name__ == "__main__":
    main()
