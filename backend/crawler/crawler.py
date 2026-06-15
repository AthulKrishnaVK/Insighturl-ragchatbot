


from collections import deque
from urllib.parse import urlparse, urldefrag
from concurrent.futures import ThreadPoolExecutor, as_completed

from crawler.scraper import (
    fetch_page,
    extract_text,
    extract_links
)


def normalize_url(url):
    clean_url, _ = urldefrag(url)
    return clean_url.rstrip("/")

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
        ".jpg",
        ".jpeg",
        ".png",
        ".gif",
        ".svg",
        ".pdf",
        ".zip",
        ".mp4",
        ".mp3",
        "#"
    ]

    for pattern in blocked_patterns:
        if pattern.lower() in link.lower():
            return False

    return True
# def is_valid_link(link):
#     blocked_patterns = [
#         "/wiki/Special:",
#         "/wiki/Talk:",
#         "/wiki/User:",
#         "/wiki/User_talk:",
#         "/wiki/File:",
#         "/wiki/Help:",
#         "/wiki/Category:",
#         "/wiki/Template:",
#         "/wiki/Template_talk:",
#         "/wiki/Portal:",
#         "/wiki/Wikipedia:",
#         "/wiki/Main_Page",
#         "action=edit",
#         "veaction=edit",
#         "#"
#     ]

#     for pattern in blocked_patterns:
#         if pattern in link:
#             return False

#     return True


def crawl_single_page(url):
    try:
        print("Crawling:", url)

        html = fetch_page(url)

        if not html:
            print("No HTML received:", url)
            return None

        print("HTML Length:", len(html))

        text = extract_text(html)

        print("Text Length:", len(text))

        links = extract_links(html, url)

        if not text.strip():
            return {
                "url": url,
                "text": "",
                "links": links
            }

        return {
            "url": url,
            "text": text,
            "links": links
        }

    except Exception as e:
        print("CRAWL PAGE ERROR:", url, e)
        return None


def crawl_website(
    start_url,
    max_pages=10,
    max_workers=5
):
    visited = set()
    queued = set()

    start_url = normalize_url(start_url)

    queue = deque([start_url])
    queued.add(start_url)

    pages = []

    base_domain = urlparse(start_url).netloc

    while queue and len(pages) < max_pages:

        batch = []

        while (
            queue
            and len(batch) < max_workers
            and len(pages) + len(batch) < max_pages
        ):
            url = queue.popleft()

            if url in visited:
                continue

            visited.add(url)
            batch.append(url)

        if not batch:
            continue

        with ThreadPoolExecutor(
            max_workers=max_workers
        ) as executor:

            future_to_url = {
                executor.submit(
                    crawl_single_page,
                    url
                ): url
                for url in batch
            }

            for future in as_completed(future_to_url):

                url = future_to_url[future]

                try:
                    result = future.result()

                    if not result:
                        continue

                    if result["text"].strip():
                        pages.append({
                            "url": result["url"],
                            "text": result["text"]
                        })

                    for link in result["links"]:

                        link = normalize_url(link)

                        if not is_valid_link(link):
                            continue

                        if (
                            urlparse(link).netloc
                            != base_domain
                        ):
                            continue

                        if link in visited:
                            continue

                        if link in queued:
                            continue

                        if (
                            len(pages)
                            + len(queue)
                            + 1
                            > max_pages
                        ):
                            continue

                        queue.append(link)
                        queued.add(link)

                except Exception as e:
                    print("CRAWL FUTURE ERROR:", url, e)

    print("Pages collected:", len(pages))

    return pages