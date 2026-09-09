import sys
import asyncio
from crawl import crawl_site_async
from rich import print


async def main() -> None:
    if len(sys.argv) < 4:
        print("usage python main.py <base_url> <max_concurrency> <max_pages>")
        sys.exit(1)
    if len(sys.argv) > 4:
        print("too many arguments provided")
        sys.exit(1)

    base_url = sys.argv[1]
    max_concurrency = sys.argv[2]
    max_pages = sys.argv[3]

    if not max_concurrency.isdigit():
        print("max_concurrency must be an integer")
        sys.exit(1)
    if not max_pages.isdigit():
        print("max_pages must be an integer")
        sys.exit(1)

    print(f"starting async crawl of: {base_url}")
    print("------------")

    page_data = await crawl_site_async(base_url, int(max_concurrency), int(max_pages))

    print("------------")

    print(f"Found {len(page_data)} pages:")
    print()
    i = 1
    for page in page_data.values():
        print(f"{i} - {page['url']} has {len(page['outgoing_links'])} outgoing links")
        i += 1

    print("------------")
    print(page_data)

    sys.exit(0)


if __name__ == "__main__":
    asyncio.run(main())
