import unittest
from crawl import (
    normalize_url,
    get_heading_from_html,
    get_first_paragraph_from_html,
    get_urls_from_html,
    get_images_from_html,
    extract_page_data,
    separate_external_internal_urls,
)


class TestCrawl(unittest.TestCase):
    # test cases for 'normalize_url' function:
    # test_1
    def test_normalize_url(self) -> None:
        input_url = "https://www.boot.dev/blog/path"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)

    # test_2
    def test_normalize_url_slash(self) -> None:
        input_url = "https://crawler-test.com/path/"
        actual = normalize_url(input_url)
        expected = "crawler-test.com/path"
        self.assertEqual(actual, expected)

    # test_3
    def test_normalize_url_capitals(self) -> None:
        input_url = "https://CRAWLER-TEST.com/path"
        actual = normalize_url(input_url)
        expected = "crawler-test.com/path"
        self.assertEqual(actual, expected)

    # test_4
    def test_normalize_url_http(self) -> None:
        input_url = "http://CRAWLER-TEST.com/path"
        actual = normalize_url(input_url)
        expected = "crawler-test.com/path"
        self.assertEqual(actual, expected)

    # test cases for 'get_heading_from_html' function:
    # test_5
    def test_get_heading_from_html_basic(self) -> None:
        input_body = """<html><body>
        <h1>Test Title</h1>
        </body></html>"""
        actual = get_heading_from_html(input_body)
        expected = "Test Title"
        self.assertEqual(actual, expected)

    # test_6
    def test_get_heading_from_html_h1h2(self) -> None:
        input_body = """<html><body>
        <h2>should not be this one</h2>
        <h1>Test Title</h1>
        </body></html>"""
        actual = get_heading_from_html(input_body)
        expected = "Test Title"
        self.assertEqual(actual, expected)

    # test_7
    def test_get_heading_from_html_h2(self) -> None:
        input_body = """<html><body>
        <h2>Test Title</h2>
        </body></html>"""
        actual = get_heading_from_html(input_body)
        expected = "Test Title"
        self.assertEqual(actual, expected)

    # test_8
    def test_get_heading_from_html_missing_h1h2(self) -> None:
        input_body = """<html><body>
        <p>Test Title</p>
        </body></html>"""
        actual = get_heading_from_html(input_body)
        expected = ""
        self.assertEqual(actual, expected)

    # test cases for 'get_first_paragraph_from_html' function:
    # test_9
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

    # test_10
    def test_get_first_paragraph_from_html_no_main(self) -> None:
        input_body = """<html><body>
            <p>paragraph 1</p>
            <p>paragraph 2</p>
        </body></html>"""
        actual = get_first_paragraph_from_html(input_body)
        expected = "paragraph 1"
        self.assertEqual(actual, expected)

    # test_11
    def test_get_first_paragraph_from_html_no_p(self) -> None:
        input_body = """<html><body>
            <h1>header 1</h1>
            <h2>header 2</h2>
        </body></html>"""
        actual = get_first_paragraph_from_html(input_body)
        expected = ""
        self.assertEqual(actual, expected)

    # test cases for 'get_urls_from_html' function:
    # test_12
    def test_get_urls_from_html_absolute(self) -> None:
        input_url = "https://crawler-test.com"
        input_body = '<html><body><a href="https://crawler-test.com"><span>Boot.dev</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com"]
        self.assertEqual(actual, expected)

    # test_13
    def test_get_urls_from_html_relative(self) -> None:
        input_url = "https://crawler-test.com"
        input_body = (
            '<html><body><a href="/path/one"><span>Boot.dev</span></a></body></html>'
        )
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/path/one"]
        self.assertEqual(actual, expected)

    # test_14
    def test_get_urls_from_html_both(self) -> None:
        input_url = "https://crawler-test.com"
        input_body = '<html><body><a href="/path/one"><span>Boot.dev</span></a><a href="https://other.com/path/one"><span>Boot.dev</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/path/one", "https://other.com/path/one"]
        self.assertEqual(actual, expected)

    # test cases for 'get_images_from_html' function:
    # test_15
    def test_get_images_from_html_absolute(self) -> None:
        input_url = "https://crawler-test.com"
        input_body = '<html><body><img src="https://crawler-test.com/logo.png" alt="Logo"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/logo.png"]
        self.assertEqual(actual, expected)

    # test_16
    def test_get_images_from_html_relative(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><img src="/logo.png" alt="Logo"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/logo.png"]
        self.assertEqual(actual, expected)

    # test_17
    def test_get_images_from_html_multiple(self) -> None:
        input_url = "https://crawler-test.com"
        input_body = '<html><body><img src="/logo.png" alt="Logo"><img src="https://cdn.boot.dev/banner.jpg"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = [
            "https://crawler-test.com/logo.png",
            "https://cdn.boot.dev/banner.jpg",
        ]
        self.assertEqual(actual, expected)

    # test cases for 'extract_page_data' function:
    # test_18
    def test_extract_page_data_basic(self):
        input_url = "https://crawler-test.com"
        input_body = """<html><body>
            <h1>Test Title</h1>
            <p>This is the first paragraph.</p>
            <a href="/link1">Link 1</a>
            <img src="/image1.jpg" alt="Image 1">
        </body></html>"""
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://crawler-test.com",
            "heading": "Test Title",
            "first_paragraph": "This is the first paragraph.",
            "total_outgoing_links": 1,
            "outgoing_links": ["https://crawler-test.com/link1"],
            "total_internal_links": 1,
            "internal_links": ["https://crawler-test.com/link1"],
            "total_external_links": 0,
            "external_links": [],
            "image_urls": ["https://crawler-test.com/image1.jpg"],
        }
        self.assertEqual(actual, expected)

    # test_19
    def test_extract_page_data_main_section(self) -> None:
        input_url = "https://crawler-test.com"
        input_body = """<html><body>
            <nav><p>Navigation paragraph</p></nav>
            <main>
                <h1>Main Title</h1>
                <p>Main paragraph content.</p>
            </main>
        </body></html>"""
        actual = extract_page_data(input_body, input_url)
        self.assertEqual(actual["heading"], "Main Title")
        self.assertEqual(actual["first_paragraph"], "Main paragraph content.")

    # test_20
    def test_extract_page_data_missing_elements(self) -> None:
        input_url = "https://crawler-test.com"
        input_body = "<html><body><div>No h1, p, links, or images</div></body></html>"
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://crawler-test.com",
            "heading": "",
            "first_paragraph": "",
            "total_outgoing_links": 0,
            "outgoing_links": [],
            "total_internal_links": 0,
            "internal_links": [],
            "total_external_links": 0,
            "external_links": [],
            "image_urls": [],
        }
        self.assertEqual(actual, expected)

    # test cases for 'separate_external_internal_urls' function:
    # test_21
    def test_separate_external_internal_urls_basic(self) -> None:
        input_url = "https://crawler-test.com"
        input_outgoing_links = [
            "https://crawler-test.com/path/one",
            "https://crawler-test.com/link1",
            "https://other.com/path/one",
        ]
        actual = separate_external_internal_urls(input_outgoing_links, input_url)
        expected = (
            [
                "https://crawler-test.com/path/one",
                "https://crawler-test.com/link1",
            ],
            ["https://other.com/path/one"],
        )
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
