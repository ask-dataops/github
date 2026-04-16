import requests
import subprocess

ORG = "your-org"
TOKEN = "ghp_xxx"

url = f"https://api.github.com/orgs/{ORG}/repos"

headers = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github+json"
}

repos = requests.get(url, headers=headers).json()

def main():
    for r in repos:
        name = r["name"]

        # filter ABC anywhere, case-insensitive
        if "abc" in name.lower():
            print(f"Processing repo: {name}")

            subprocess.run([
                "python",
                "webhook_to_csv_v2.py",
                name
            ])

if __name__ == "__main__":
    main()
