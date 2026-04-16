import requests
import csv

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

    filename = "abc_repos.csv"

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        # Header
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

                if not name.lower().startswith("abc"):
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

            page += 1

    print(f"\nDone. Total ABC repos exported: {count}")
    print(f"CSV file: {filename}")


if __name__ == "__main__":
    main()
