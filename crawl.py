from urllib.parse import urlsplit, urljoin
from bs4 import BeautifulSoup, Tag
from typing import TypedDict

# import requests
import asyncio
import aiohttp
from types import TracebackType


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


def get_urls_from_html(html: str, base_url: str) -> list[str]:
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


def get_images_from_html(html: str, base_url: str) -> list[str]:
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


class AsyncCrawler:
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url
        self.base_domain = urlsplit(base_url).netloc
        self.page_data: dict[str, PageData] = {}
        self.lock = asyncio.Lock()
        self.max_concurrency = 5
        self.semaphore = asyncio.Semaphore(self.max_concurrency)
        self.session: aiohttp.ClientSession() | None = None

    async def __aenter__(self) -> "AsyncCrawler":
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        if self.session is not None:
            await self.session.close()

    async def add_page_visit(self, normalized_url: str) -> bool:
        async with self.lock:
            if normalized_url in self.page_data:
                return False
            else:
                return True

    async def get_html(self, url: str) -> str | None:
        if self.session is None:
            return None

        try:
            async with self.session.get(
                url, headers={"User-Agent": "myCrawler_learning/1.0"}
            ) as response:
                if response.status > 399:
                    print(f"Error: HTTP error: {response.status} for {url}")
                    return None

                content_type = response.headers.get("content-type", "")
                if "text/html" not in content_type:
                    print(
                        f"Error: Expected text/html, but got: {content_type} for {url}"
                    )
                    return None

                return await response.text()
        except Exception as e:
            print(f"Error: network error while fetching {url}: {e}")
            return None

    async def crawl_page(self, current_url: str) -> None:
        if urlsplit(current_url).netloc != self.base_domain:
            return

        normalized_url = normalize_url(current_url)

        is_new = await self.add_page_visit(normalized_url)
        if not is_new:
            return

        async with self.semaphore:
            print(
                f"Crawling {current_url} (Active: {self.max_concurrency - self.semaphore._value})"
            )
            html = await self.get_html(current_url)
            if html is None:
                return

            page_info = extract_page_data(html, current_url)
            async with self.lock:
                self.page_data[normalized_url] = page_info

            next_urls = get_urls_from_html(html, self.base_url)

        tasks: list[asyncio.Task[None]] = []
        for next_url in next_urls:
            tasks.append(asyncio.create_task(self.crawl_page(next_url)))

        if tasks:
            await asyncio.gather(*tasks)

    async def crawl(self) -> dict[str, PageData]:
        await self.crawl_page(self.base_url)
        return self.page_data


async def crawl_site_async(base_url: str) -> dict[str, PageData]:
    async with AsyncCrawler(base_url) as crawler:
        return await crawler.crawl()


## ---->> these blocks of code below are synchronous using requests library <<----

# def get_html(url: str) -> str:
#     try:
#         response = requests.get(url, headers={"User-Agent": "myCrawler/1.0"})
#     except Exception as e:
#         print(f"network error while fetching {url}: {e}")

#     if response.status_code > 399:
#         raise Exception(f"got HTTP error: {response.status_code} {response.reason}")

#     content_type = response.headers.get("content-type", "")
#     if "text/html" not in content_type:
#         raise Exception(f"Expected text/html, but got: {content_type}")

#     return response.text


# def safe_get_html(url: str) -> str | None:
#     try:
#         return get_html(url)
#     except Exception as e:
#         print(f"{e}")
#         return None


# def crawl_page(
#     base_url: str,
#     current_url: str | None = None,
#     page_data: dict[str, PageData] | None = None,
# ) -> dict[str, PageData]:
#     if current_url is None:
#         current_url = base_url
#     if page_data is None:
#         page_data = {}

#     base_url_obj = urlsplit(base_url)
#     current_url_obj = urlsplit(current_url)
#     if current_url_obj.netloc != base_url_obj.netloc:
#         return page_data

#     normalized_url = normalize_url(current_url)

#     if normalized_url in page_data:
#         return page_data

#     print(f"crawling {current_url}")
#     html = safe_get_html(current_url)
#     if html is None:
#         return page_data

#     page_info = extract_page_data(html, current_url)
#     page_data[normalized_url] = page_info

#     next_urls = get_urls_from_html(html, base_url)
#     for next_url in next_urls:
#         page_data = crawl_page(base_url, next_url, page_data)

#     return page_data

## ---->> these blocks of code above are synchronous using requests library <<----
