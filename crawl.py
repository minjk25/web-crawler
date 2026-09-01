from urllib.parse import urlsplit, urljoin
from bs4 import BeautifulSoup, Tag
from typing import TypedDict


class PageData(TypedDict):
    url: str
    heading: str
    first_paragraph: str
    outgoing_links: list[str]
    image_urls: list[str]


def normalize_url(url: str) -> str:
    parsed_url = urlsplit(url)
    return f"{parsed_url.netloc}{parsed_url.path}".rstrip("/").lower()


def get_heading_from_html(html: str) -> str:
    beautiful_html = BeautifulSoup(html, "html.parser")
    h_tag = beautiful_html.find("h1")
    if not h_tag:
        h_tag = beautiful_html.find("h2")

    return h_tag.get_text(strip=True) if isinstance(h_tag, Tag) else ""


def get_first_paragraph_from_html(html: str) -> str:
    beautiful_html = BeautifulSoup(html, "html.parser")
    main_tag = beautiful_html.find("main")
    if not isinstance(main_tag, Tag):
        first_p = beautiful_html.find("p")
    else:
        first_p = main_tag.find("p")

    return first_p.get_text(strip=True) if isinstance(first_p, Tag) else ""


def get_urls_from_html(html, base_url):
    beautiful_html = BeautifulSoup(html, "html.parser")
    a_tag = beautiful_html.find_all("a")
    result = []

    for a in a_tag:
        if not isinstance(a, Tag):
            continue

        href = a.get("href")
        if isinstance(href, str) and href:
            try:
                result.append(urljoin(base_url, href))
            except Exception as e:
                print(f"Error joining URL -> {str(e)}: {href}")

    return result


def get_images_from_html(html, base_url):
    beautiful_html = BeautifulSoup(html, "html.parser")
    img_tag = beautiful_html.find_all("img")
    result = []

    for img in img_tag:
        if not isinstance(img, Tag):
            continue

        src = img.get("src")
        if isinstance(src, str) and src:
            try:
                result.append(urljoin(base_url, src))
            except Exception as e:
                print(f"Error joining URL -> {str(e)}: {src}")

    return result


def extract_page_data(html: str, page_url: str) -> PageData:
    return {
        "url": page_url,
        "heading": get_heading_from_html(html),
        "first_paragraph": get_first_paragraph_from_html(html),
        "outgoing_links": get_urls_from_html(html, page_url),
        "image_urls": get_images_from_html(html, page_url),
    }
