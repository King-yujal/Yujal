import json
import time
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup


class YujalCrawler:

    def __init__(self, seed_url, max_pages=15):
        self.seed_url = seed_url
        self.max_pages = max_pages
        self.visited = set()
        self.search_index = []  # Stores our crawled page details

    def crawl(self):
        frontier = [self.seed_url]

        while frontier and len(self.visited) < self.max_pages:
            url = frontier.pop(0)
            if url in self.visited:
                continue

            print(f"🕸️ Crawling: {url}")
            self.visited.add(url)

            try:
                response = requests.get(
                    url, headers={"User-Agent": "YujalBot/1.0"}, timeout=5
                )
                if response.status_code != 200 or "text/html" not in response.headers.get(
                    "Content-Type", ""
                ):
                    continue

                soup = BeautifulSoup(response.text, "html.parser")

                # Extract Text Content
                title = soup.title.string.strip() if soup.title else url
                # Get the first paragraph or generic body text as snippet
                first_p = soup.find("p")
                snippet = (
                    first_p.text.strip()[:150]
                    if first_p
                    else "No description available."
                )

                # Append data payload to our search index
                self.search_index.append(
                    {"url": url, "title": title, "snippet": snippet}
                )

                # Discover Internal Links to crawl next
                for link in soup.find_all("a", href=True):
                    full_url = urljoin(url, link["href"])
                    parsed = urlparse(full_url)

                    # --- FIXED INDENTATION SPACES RIGHT HERE ---
                    if (
                        parsed.scheme in ["http", "https"]
                        and "wikipedia.org" in parsed.netloc
                    ):
                        clean_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
                        if clean_url not in self.visited:
                            frontier.append(clean_url)

                time.sleep(1)  # Polite delay

            except Exception as e:
                print(f"❌ Error indexing {url}: {e}")

        # Save indexed database to local JSON file
        with open("search_index.json", "w", encoding="utf-8") as f:
            json.dump(self.search_index, f, indent=4)
        print(f"\n✅ Crawling complete! Saved {len(self.search_index)} pages.")


if __name__ == "__main__":
    # Target the deep English reading portal straight away so it doesn't get stuck
    bot = YujalCrawler("https://wikipedia.org", max_pages=15)
    bot.crawl()