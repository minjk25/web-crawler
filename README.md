# Web Crawler

A simple Python web crawler that extracts headings, links, and images from a site and exports the results as a structured JSON report.

## Overview

This project is a simple, configurable web crawler built in Python. It starts from a given URL, recursively follows internal links up to a specified depth,
and collects structured data from each page it visits including page headings, first paragraphs, outgoing links, and image URLs.

Once crawling is complete, the collected data is exported to a `report.json` file, making it easy to inspect, share, or process further.

### Features

- Recursively crawls a website starting from a base URL
- Limits crawling by maximum depth and/or maximum number of pages
- Normalizes URLs to avoid revisiting duplicate pages
- Extracts key page data (heading, first paragraph, links, images)
- Exports all collected data as a structured JSON report

## Requirements

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) installed

## Installation

1. Clone the repository
   ```bash
   git clone https://github.com/minjk25/web-crawler.git

   cd web-crawler
   ```
2. Install dependencies using [uv](https://github.com/astral-sh/uv):
   ```bash
   uv sync
   ```
## Usage

```bash
uv run main.py <your website to be crawled>
```

Optional arguments:
- `--max_concur <int>` – A maximum concurrency to limit the number of requests allowed at once (e.g., `--max_concur 5`)
- `--max_pages <int>` – A maximum number of pages to crawl (e.g., `--max_pages 25`)
- `--verbose <str: result, report, all>` – Show more details of web crawling (e.g., `--verbose report`)

### Example:

Ex.1: crawl `https://learnwebscraping.dev/practice/ecommerce/` (with default max_concur = 3 and max_pages = all)
```bash
uv run main.py https://learnwebscraping.dev/practice/ecommerce/
```

Ex.2: crawl `https://learnwebscraping.dev/practice/ecommerce/` with max_concur = 5, max_pages = 25 and show report details
```bash
uv run main.py https://learnwebscraping.dev/practice/ecommerce/ --max_concur 5 --max_pages 25 --verbose report
```

### Note:
If crawling takes too long (which can happen when a page has many internal links), you can explicitly stop the program at any time with `Ctrl + C`

## Documentation & Resources
- [What is a web crawler?](https://www.cloudflare.com/learning/bots/what-is-a-web-crawler/)
- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [asyncio](https://docs.python.org/3/library/asyncio.html)
- [aiohttp](https://docs.aiohttp.org/en/stable/client_reference.html#client-session)
- [Boot.dev](https://boot.dev)
