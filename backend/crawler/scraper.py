import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os


def fetch_page(url):
    try:
        print("Fetching:", url)

        response = requests.get(
            url,
            timeout=10,
            headers={
                "User-Agent":
                "Mozilla/5.0"
            }
        )

        print("Status:", response.status_code)

        if response.status_code == 200:
            return response.text

    except Exception as e:
        print("Error:", e)

    return None

def extract_text(html):
    soup = BeautifulSoup(html, "html.parser")

    return soup.get_text(separator=" ", strip=True)


def extract_links(html, base_url):
    soup = BeautifulSoup(html, "html.parser")

    links = set()

    for tag in soup.find_all("a", href=True):

        full_url = urljoin(base_url, tag["href"])

        links.add(full_url)

    return links

if __name__ == "__main__":

    url = "https://example.com"

    html = fetch_page(url)

    links = extract_links(html, url)

    print(links)