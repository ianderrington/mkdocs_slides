import pytest
from mkdocs_slides.plugin import SlidesPlugin
from mkdocs_slides.slide_parser import SlideParser

def test_basic_slide_parsing():
    parser = SlideParser()
    # Add your tests here 