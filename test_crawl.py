import unittest
from crawl import normalize_url
from crawl import get_heading_from_html
from crawl import get_first_paragraph_from_html


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
    def test_get_heading_from_html_basic(self):
        input_body = """<html><body>
        <h1>Test Title</h1>
        </body></html>"""
        actual = get_heading_from_html(input_body)
        expected = "Test Title"
        self.assertEqual(actual, expected)

    def test_get_heading_from_html_h1h2(self):
        input_body = """<html><body>
        <h2>should not be this one</h2>
        <h1>Test Title</h1>
        </body></html>"""
        actual = get_heading_from_html(input_body)
        expected = "Test Title"
        self.assertEqual(actual, expected)

    def test_get_heading_from_html_h2(self):
        input_body = """<html><body>
        <h2>Test Title</h2>
        </body></html>"""
        actual = get_heading_from_html(input_body)
        expected = "Test Title"
        self.assertEqual(actual, expected)

    def test_get_heading_from_html_missing_h1h2(self):
        input_body = """<html><body>
        <p>Test Title</p>
        </body></html>"""
        actual = get_heading_from_html(input_body)
        expected = ""
        self.assertEqual(actual, expected)

    # test cases for 'get_first_paragraph_from_html' function:
    def test_get_first_paragraph_from_html_main_priority(self):
        input_body = """<html><body>
            <p>Outside paragraph.</p>
            <main>
                <p>Main paragraph.</p>
            </main>
        </body></html>"""
        actual = get_first_paragraph_from_html(input_body)
        expected = "Main paragraph."
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html_no_main(self):
        input_body = """<html><body>
            <p>paragraph 1</p>
            <p>paragraph 2</p>
        </body></html>"""
        actual = get_first_paragraph_from_html(input_body)
        expected = "paragraph 1"
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html_no_p(self):
        input_body = """<html><body>
            <h1>header 1</h1>
            <h2>header 2</h2>
        </body></html>"""
        actual = get_first_paragraph_from_html(input_body)
        expected = ""
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
