


import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def fetch_page(url):
    try:
        print("Fetching:", url)

        response = requests.get(
            url,
            timeout=5,
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

    for tag in soup([
        "script",
        "style",
        "nav",
        "footer",
        "header",
        "aside",
        "noscript"
    ]):
        tag.decompose()

    content = []

    for tag in soup.find_all(
        ["h1", "h2", "h3", "p", "li", "table"]
    ):

        if tag.name == "table":

            rows = []

            for row in tag.find_all("tr"):

                cells = [
                    cell.get_text(" ", strip=True)
                    for cell in row.find_all(["th", "td"])
                ]

                if cells:
                    rows.append(" | ".join(cells))

            if rows:
                content.append(
                    "TABLE:\n" + "\n".join(rows)
                )

        else:
            text = tag.get_text(" ", strip=True)

            if text:
                content.append(text)

    return "\n\n".join(content)


def extract_links(html, base_url):
    soup = BeautifulSoup(html, "html.parser")

    links = set()

    for tag in soup.find_all("a", href=True):

        full_url = urljoin(
            base_url,
            tag["href"]
        )

        links.add(full_url)

    return links


if __name__ == "__main__":

    url = "https://example.com"

    html = fetch_page(url)

    if html:
        text = extract_text(html)
        links = extract_links(html, url)

        print(text[:1000])
        print(links)