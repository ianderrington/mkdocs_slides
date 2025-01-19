import pytest

from mkdocs_slides.plugin import SlidesPlugin
from mkdocs_slides.slide_parser import SlideParser


def test_slide_parser_initialization():
    parser = SlideParser()
    assert parser is not None


def test_basic_slide_config():
    parser = SlideParser()
    test_markdown = """```slides
    title: Test Deck
    url_stub: test
    nav:
        - test/slide1.md
    ```"""
    config = {"docs_dir": "docs", "site_dir": "site"}
    # This will need mocking for file operations
    # result = parser.process_markdown(test_markdown, None, config)
    # assert 'slides-deck' in result
