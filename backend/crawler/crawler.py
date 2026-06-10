from collections import deque
from urllib.parse import urlparse
import json
from crawler.scraper import (
    fetch_page,
    extract_text,
    extract_links
)


def crawl_website(start_url, max_pages=10):

    visited = set()

    queue = deque([start_url])

    pages = []

    base_domain = urlparse(start_url).netloc

    while queue and len(visited) < max_pages:

        url = queue.popleft()

        if url in visited:
            continue

        print("Crawling:", url)
        html = fetch_page(url)

        if not html:
           print("No HTML received")
           continue

        print("HTML Length:", len(html))
        # html = fetch_page(url)

       
        text = extract_text(html)

        print("Text Length:", len(text))

        pages.append({
            "url": url,
            "text": text
        })

        visited.add(url)

        links = extract_links(html, url)

        for link in links:

            if urlparse(link).netloc == base_domain:

                if link not in visited:
                    queue.append(link)
    print("Pages collected:", len(pages))
    return pages

