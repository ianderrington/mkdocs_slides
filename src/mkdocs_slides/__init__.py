import os
from pathlib import Path

from mkdocs.config import config_options
from mkdocs.plugins import BasePlugin
from mkdocs.structure.files import File

from .slide_parser import SlideParser


class SlidesPlugin(BasePlugin):
    config_scheme = (
        ("padding", config_options.Type(str, default="64px")),
        ("max_width", config_options.Type(str, default="1200px")),
        ("aspect_ratio", config_options.Type(str, default="16/9")),
        ("font_size", config_options.Type(str, default="32px")),
        ("template", config_options.Type(str, default=None)),
    )

    def __init__(self):
        super().__init__()
        self.parser = SlideParser()

    def on_files(self, files, config):
        """Register static assets"""
        static_dir = os.path.join(os.path.dirname(__file__), "static")

        # Add CSS file
        css_file = File(
            path="slides.css",
            src_dir=os.path.join(static_dir, "css"),
            dest_dir=os.path.join(config["site_dir"], "assets", "slides", "css"),
            use_directory_urls=False,
        )
        files.append(css_file)

        # Add JS file
        js_file = File(
            path="slides.js",
            src_dir=os.path.join(static_dir, "js"),
            dest_dir=os.path.join(config["site_dir"], "assets", "slides", "js"),
            use_directory_urls=False,
        )
        files.append(js_file)

        print(f"Adding slides.js from {js_file.src_path} to {js_file.dest_path}")
        return files

    def on_config(self, config):
        """Add our javascript and pass configuration"""
        if "extra_javascript" not in config:
            config["extra_javascript"] = []
        if "extra_css" not in config:
            config["extra_css"] = []

        config["extra_javascript"].append("assets/slides/js/slides.js")
        config["extra_css"].append("assets/slides/css/slides.css")

        # Pass plugin config to parser
        self.parser.set_config(self.config)

        # Pass custom template path if provided
        if self.config.get("template"):
            template_path = os.path.abspath(self.config["template"])
            if not os.path.exists(template_path):
                print(f"Warning: Custom template {template_path} not found, using default")
            else:
                print(f"Using custom template {template_path}")
                self.parser.set_template(template_path)

        return config

    def on_page_markdown(self, markdown, page, config, files):
        """Process the markdown content and replace slides blocks with HTML"""
        try:
            processed_markdown = self.parser.process_markdown(
                markdown=markdown, page=page, config=config
            )

            if "```slides" in markdown:
                self.parser.write_files()

            return processed_markdown
        except Exception as e:
            print(f"Error processing slides in {page.file.src_path}: {str(e)}")
            return markdown


def get_plugin():
    return SlidesPlugin


# Make sure these are directly importable
__all__ = ["SlidesPlugin", "get_plugin"]
