from collections import deque
from urllib.parse import urlparse, urldefrag

from crawler.scraper import (
    fetch_page,
    extract_text,
    extract_links
)


def normalize_url(url):
    clean_url, _ = urldefrag(url)
    return clean_url


def is_valid_link(link):

    blocked_patterns = [
        "/wiki/Special:",
        "/wiki/Talk:",
        "/wiki/User:",
        "/wiki/User_talk:",
        "/wiki/File:",
        "/wiki/Help:",
        "/wiki/Category:",
        "/wiki/Template:",
        "/wiki/Template_talk:",
        "/wiki/Portal:",
        "/wiki/Wikipedia:",
        "/wiki/Main_Page",
        "action=edit",
        "veaction=edit",
        "?",
        "#"
    ]

    for pattern in blocked_patterns:
        if pattern in link:
            return False

    return True


def crawl_website(start_url, max_pages=10):

    visited = set()
    queued = set()

    start_url = normalize_url(start_url)

    queue = deque([start_url])
    queued.add(start_url)

    pages = []

    base_domain = urlparse(start_url).netloc

    while queue and len(pages) < max_pages:

        url = queue.popleft()

        if url in visited:
            continue

        print("Crawling:", url)

        html = fetch_page(url)

        if not html:
            print("No HTML received")
            continue

        print("HTML Length:", len(html))

        text = extract_text(html)

        print("Text Length:", len(text))

        if text.strip():
            pages.append({
                "url": url,
                "text": text
            })

        visited.add(url)

        links = extract_links(html, url)

        for link in links:

            link = normalize_url(link)

            if not is_valid_link(link):
                continue

            if urlparse(link).netloc != base_domain:
                continue

            if link in visited:
                continue

            if link in queued:
                continue

            queue.append(link)
            queued.add(link)

    print("Pages collected:", len(pages))

    return pages