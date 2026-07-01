import argparse
import urllib.request
import urllib.parse
import datetime
import json

date = datetime.datetime.now()

base_url = "https://api.github.com/search/repositories"

def search_trending_repos(duration, limit):
    if duration == 'day':
        start_date = (date - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    elif duration == 'month':
        start_date = (date - datetime.timedelta(days=30)).strftime("%Y-%m-%d")
    else: # week
        start_date = (date - datetime.timedelta(days=7)).strftime("%Y-%m-%d")
    query = f"created:>{start_date}"
    params = {'q': query, 'sort': 'stars', 'order': 'desc'}
    url = f"{base_url}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'}) #pentru a nu da eroare 403 Forbideen ii spunem ca suntem un browser nu un robot
    with urllib.request.urlopen(req) as response:
        raw_data = response.read()
        repositories = json.loads(raw_data.decode())
        print(f"DEBUG: Am găsit {len(repositories.get('items', []))} repozitorii.")
        print(f"{'Name':<20} {'Description':<20} {'Stars':<10} {'Language':<10}")
        for r in repositories.get('items', [])[:limit]:
            name = (r.get('name') or "N/A")[:17] + "..."
            desc = (r.get('description') or "N/A")[:17] + "..." # ia doar primele 17 caractere
            stars = r.get('stargazers_count', 0)
            lang = r.get('language') or "N/A"

            print(f"{name:<20} {desc:<20} {stars:<10} {lang:<10}")

def main():
    parser = argparse.ArgumentParser(description = "Tool for trending repos on GitHub")
    parser.add_argument("--duration", choices = ['day', 'week', 'month'], default = 'week')
    parser.add_argument("--limit", type = int, default = 10)

    args = parser.parse_args()
    search_trending_repos(args.duration, args.limit)

if __name__ == "__main__":
    main()