import os
import shutil

from mkdocs.plugins import BasePlugin
from mkdocs.structure.files import File

from .renderer import SlideRenderer
from .slide_parser import SlideParser


class SlidesPlugin(BasePlugin):
    def __init__(self):
        self.parser = SlideParser()
        self.renderer = SlideRenderer()
        self.slides_to_write = []  # Store slide HTML content to write during build

    def on_config(self, config):
        """Set up the plugin configuration"""
        return config

    def on_files(self, files, config):
        """Add slide HTML files to the build"""
        # Add our static files
        static_path = os.path.join(os.path.dirname(__file__), "static")

        css_file = files.get_file_from_path("assets/slides/css/slides.css")
        if not css_file:
            files.append_file(
                path="assets/slides/css/slides.css",
                src_dir=os.path.join(static_path, "css"),
                dest_dir=os.path.join(config["site_dir"], "assets/slides/css"),
                use_directory_urls=False,
            )

        js_file = files.get_file_from_path("assets/slides/js/slides.js")
        if not js_file:
            files.append_file(
                path="assets/slides/js/slides.js",
                src_dir=os.path.join(static_path, "js"),
                dest_dir=os.path.join(config["site_dir"], "assets/slides/js"),
                use_directory_urls=False,
            )

        # Add slide HTML files
        for slide in self.slides_to_write:
            # Create a proper MkDocs File object
            file_path = os.path.join(config["docs_dir"], slide["path"])
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(slide["content"])

            slide_file = File(
                path=slide["path"],
                src_dir=config["docs_dir"],
                dest_dir=config["site_dir"],
                use_directory_urls=False,
            )
            files.append(slide_file)

        return files

    def on_page_markdown(self, markdown, page, config, files):
        """Process the markdown content and replace slides blocks with HTML"""
        try:
            # Clear previous slides
            self.slides_to_write = []

            # Process markdown and collect slides
            processed_markdown = self.parser.process_markdown(
                markdown,
                page.file.src_path,
                config,
                self.slides_to_write,  # Pass list to collect slides
            )

            if "```slides" in markdown:
                # Only inject CSS/JS if the page contains slides
                page.head_extra = [
                    '<link rel="stylesheet" href="/assets/slides/css/slides.css">',
                    '<script src="/assets/slides/js/slides.js"></script>',
                ]
            return processed_markdown
        except Exception as e:
            print(f"Error processing slides in {page.file.src_path}: {str(e)}")
            return markdown
