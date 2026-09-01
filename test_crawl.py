import unittest
from crawl import (
    normalize_url,
    get_heading_from_html,
    get_first_paragraph_from_html,
    get_urls_from_html,
    get_images_from_html,
)


class TestCrawl(unittest.TestCase):
    # test cases for 'normalize_url' function:
    def test_normalize_url(self) -> None:
        input_url = "https://www.boot.dev/blog/path"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)

    def test_normalize_url_slash(self) -> None:
        input_url = "https://crawler-test.com/path/"
        actual = normalize_url(input_url)
        expected = "crawler-test.com/path"
        self.assertEqual(actual, expected)

    def test_normalize_url_capitals(self) -> None:
        input_url = "https://CRAWLER-TEST.com/path"
        actual = normalize_url(input_url)
        expected = "crawler-test.com/path"
        self.assertEqual(actual, expected)

    def test_normalize_url_http(self) -> None:
        input_url = "http://CRAWLER-TEST.com/path"
        actual = normalize_url(input_url)
        expected = "crawler-test.com/path"
        self.assertEqual(actual, expected)

    # test cases for 'get_heading_from_html' function:
    def test_get_heading_from_html_basic(self) -> None:
        input_body = """<html><body>
        <h1>Test Title</h1>
        </body></html>"""
        actual = get_heading_from_html(input_body)
        expected = "Test Title"
        self.assertEqual(actual, expected)

    def test_get_heading_from_html_h1h2(self) -> None:
        input_body = """<html><body>
        <h2>should not be this one</h2>
        <h1>Test Title</h1>
        </body></html>"""
        actual = get_heading_from_html(input_body)
        expected = "Test Title"
        self.assertEqual(actual, expected)

    def test_get_heading_from_html_h2(self) -> None:
        input_body = """<html><body>
        <h2>Test Title</h2>
        </body></html>"""
        actual = get_heading_from_html(input_body)
        expected = "Test Title"
        self.assertEqual(actual, expected)

    def test_get_heading_from_html_missing_h1h2(self) -> None:
        input_body = """<html><body>
        <p>Test Title</p>
        </body></html>"""
        actual = get_heading_from_html(input_body)
        expected = ""
        self.assertEqual(actual, expected)

    # test cases for 'get_first_paragraph_from_html' function:
    def test_get_first_paragraph_from_html_main_priority(self) -> None:
        input_body = """<html><body>
            <p>Outside paragraph.</p>
            <main>
                <p>Main paragraph.</p>
            </main>
        </body></html>"""
        actual = get_first_paragraph_from_html(input_body)
        expected = "Main paragraph."
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html_no_main(self) -> None:
        input_body = """<html><body>
            <p>paragraph 1</p>
            <p>paragraph 2</p>
        </body></html>"""
        actual = get_first_paragraph_from_html(input_body)
        expected = "paragraph 1"
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html_no_p(self) -> None:
        input_body = """<html><body>
            <h1>header 1</h1>
            <h2>header 2</h2>
        </body></html>"""
        actual = get_first_paragraph_from_html(input_body)
        expected = ""
        self.assertEqual(actual, expected)

    # test cases for 'get_urls_from_html' function:
    def test_get_urls_from_html_absolute(self) -> None:
        input_url = "https://crawler-test.com"
        input_body = '<html><body><a href="https://crawler-test.com"><span>Boot.dev</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com"]
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_relative(self) -> None:
        input_url = "https://crawler-test.com"
        input_body = (
            '<html><body><a href="/path/one"><span>Boot.dev</span></a></body></html>'
        )
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/path/one"]
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_both(self) -> None:
        input_url = "https://crawler-test.com"
        input_body = '<html><body><a href="/path/one"><span>Boot.dev</span></a><a href="https://other.com/path/one"><span>Boot.dev</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/path/one", "https://other.com/path/one"]
        self.assertEqual(actual, expected)

    # test cases for 'get_images_from_html' function:
    def test_get_images_from_html_absolute(self) -> None:
        input_url = "https://crawler-test.com"
        input_body = '<html><body><img src="https://crawler-test.com/logo.png" alt="Logo"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/logo.png"]
        self.assertEqual(actual, expected)

    def test_get_images_from_html_relative(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><img src="/logo.png" alt="Logo"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/logo.png"]
        self.assertEqual(actual, expected)

    def test_get_images_from_html_multiple(self) -> None:
        input_url = "https://crawler-test.com"
        input_body = '<html><body><img src="/logo.png" alt="Logo"><img src="https://cdn.boot.dev/banner.jpg"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = [
            "https://crawler-test.com/logo.png",
            "https://cdn.boot.dev/banner.jpg",
        ]
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
