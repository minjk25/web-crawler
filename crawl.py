from urllib.parse import urlsplit
from bs4 import BeautifulSoup, Tag


def normalize_url(url: str) -> str:
    parsed_url = urlsplit(url)
    return f"{parsed_url.hostname}{parsed_url.path}".rstrip("/")


def get_heading_from_html(html: str) -> str:
    beautifu_html = BeautifulSoup(html, "html.parser")
    h_tag = beautifu_html.find("h1")
    if not h_tag:
        h_tag = beautifu_html.find("h2")

    return h_tag.get_text(strip=True) if isinstance(h_tag, Tag) else ""


def get_first_paragraph_from_html(html: str) -> str:
    beautifu_html = BeautifulSoup(html, "html.parser")
    main_tag = beautifu_html.find("main")
    if not main_tag:
        first_p = beautifu_html.find("p")
    else:
        first_p = main_tag.find("p")

    return first_p.get_text(strip=True) if isinstance(first_p, Tag) else ""
