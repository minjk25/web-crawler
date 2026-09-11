import sys
import asyncio
from crawl import crawl_site_async
from rich import print
from json_report import write_json_report
import argparse
from rich.console import Console

console = Console()


async def main() -> None:
    parser = argparse.ArgumentParser(
        description="A simple web crawler. "
        "Usage: uv main.py <base_url> <Optional: max_concurrency> <Optional: max_pages>"
    )
    parser.add_argument("base_url", help="A base url to crawl")
    parser.add_argument(
        "--max_concur",
        type=int,
        default=3,
        help="A maximum concurrency to limit the number of requests allowed at once (e.g., --max_concur 5)",
    )
    parser.add_argument(
        "--max_pages",
        type=int,
        default=float("inf"),
        help="A maximum number of pages to crawl (e.g., --max_pages 25)",
    )
    parser.add_argument("--v", action="store_true", help="Show details of web crawling")

    args = parser.parse_args()

    base_url = args.base_url
    max_concurrency = args.max_concur
    max_pages = args.max_pages
    verbose = args.v

    print(f"starting async crawl of: {base_url}")
    print()

    with console.status("[bold green]Crawling...\n", spinner="dots"):
        page_data = await crawl_site_async(base_url, max_concurrency, max_pages)

    print()
    print(f"Crawling complete. Found {len(page_data)} pages.")
    write_json_report(page_data)

    if verbose:
        print()
        print("------------------------------------------------")
        print("The result of web crawling:")
        print()

        i = 1
        for page in page_data.values():
            print(
                f"{i} - {page['url']} has {len(page['outgoing_links'])} outgoing links"
            )
            i += 1

        print()
        print("------------------------------------------------")
        print("The details of the report:")
        print()
        print(page_data)
        print()
        print("------------------------------------------------")

    sys.exit(0)


if __name__ == "__main__":
    asyncio.run(main())
