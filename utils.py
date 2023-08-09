from typing import Optional, List

from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from playwright.async_api import async_playwright
from html2text import html2text


def fetch_html(
    url: str, remove_selectors: Optional[List[str]] = None, headless=True
) -> str:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        page = browser.new_page()
        page.goto(url, wait_until="domcontentloaded")

        for selector in remove_selectors or []:
            elements = page.locator(selector).all()
            for element in elements:
                if element.is_visible():
                    element.evaluate("element => element.remove()")

        page_source = page.content()
        browser.close()

        return page_source


async def fetch_html_async(
    url: str, remove_selectors: Optional[List[str]] = None, headless=True
) -> str:
    async with async_playwright() as playwright:
        chromium = playwright.chromium  # or "firefox" or "webkit".
        browser = await chromium.launch(headless=headless)
        page = await browser.new_page()
        await page.goto(url, wait_until="domcontentloaded")

        for selector in remove_selectors or []:
            elements = page.locator(selector).all()
            for element in elements:
                if element.is_visible():
                    await element.evaluate("element => element.remove()")

        page_source = await page.content()
        await browser.close()

        return page_source


def preprocess_html(html: str) -> str:
    soup = BeautifulSoup(
        "".join(s.strip() for s in html.split("\n")),
        "html.parser",
    )

    for s in soup.select("script"):
        s.extract()
    for s in soup.select("style"):
        s.extract()

    # add divider between siblings of the same type
    def add_divider(node, threshold):
        if isinstance(node, str):
            return
        tags = set()
        children_count = set()

        if not hasattr(node, "children"):
            return

        for child in node.children:
            if child == "\n":
                child.decompose()

            add_divider(child, threshold)  # pylint: disable=cell-var-from-loop
            tags.add(child.name)
            if hasattr(child, "contents"):
                children_count.add(len(child.contents))

        if (
            node.name
            not in {
                "ul",
                "ol",
                "table",
                "tbody",
                "thead",
                "tr",
                "td",
                "th",
            }
            and len(tags) == 1
            and len(children_count) == 1
            and len(node.contents) >= threshold
        ):
            for i in range(-len(node.contents) + 1, 0, 1):
                new_tag = soup.new_tag("p")  # pylint: disable=cell-var-from-loop
                new_tag.string = "---"
                node.insert(i, new_tag)

    add_divider(soup.body, 3)
    simple_tree = soup.prettify()

    # html2text is used to convert html to markdown
    text = html2text(str(simple_tree))
    return text


def get_chunks(
    s: str, chunk_size: int, chunk_overlap: int, seperator: str = "\n"
) -> List[str]:
    """returns an iterator of segments of s with chunk_size and chunk_overlap"""
    if chunk_size < 1:
        raise ValueError("chunk_size must be greater than 0")
    if chunk_overlap < 0:
        raise ValueError("chunk_overlap must be greater than or equal to 0")
    if chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap must be less than chunk_size")
    if not seperator:
        raise ValueError("seperator must be a character")

    segments = []
    segments_size = 0
    for segment in s.split(seperator):
        if segments_size + len(segment) > chunk_size:
            yield seperator.join(segments)
            while segments_size - len(segments[0]) >= chunk_overlap:
                segments_size -= len(segments[0])
                segments.pop(0)
        segments.append(segment)
        segments_size += len(segment)
    yield seperator.join(segments)


def flatten(html: str) -> str:
    soup = BeautifulSoup(
        "".join(s.strip() for s in html.split("\n")),
        "html.parser",
    )

    for tag in ["script", "style", "meta", "link", "path"]:
        for s in soup.select(tag):
            s.decompose()

    # flatten any single child elements
    def flatten(node):
        if isinstance(node, str):
            return
        for child in node.children:
            flatten(child)
        if len(node.contents) == 1:
            node.unwrap()
            # child = node.contents[0]
            # child.unwrap()

    flatten(soup.html)
    return "\n".join(s.strip() for s in soup.prettify().split("\n"))
