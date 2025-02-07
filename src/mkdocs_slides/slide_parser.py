import glob
import os
import re
from pathlib import Path

import jinja2
import yaml
from markdown import Markdown


class SlideParser:
    def __init__(self):
        self.slides_pattern = re.compile(r"```slides\s*(.*?)```", re.DOTALL)
        self.template_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader([
                os.path.join(os.path.dirname(__file__), "templates"),
                os.path.curdir  # Allow loading from current directory
            ])
        )
        self.template_name = "slide_template.html"  # Default template
        self.slide_template = self.template_env.get_template(self.template_name)
        self.files_to_write = []  # Store files that need to be written
        # Default configuration
        self.config = {
            "padding": "64px",
            "max_width": "1200px",
            "aspect_ratio": "16/9",
            "font_size": "32px",  # Updated default
        }

    def set_config(self, config):
        # Update defaults with any provided config values
        if config:
            self.config.update(config)

    def set_template(self, template_path):
        """Set a custom template path"""
        template_dir = os.path.dirname(template_path)
        template_name = os.path.basename(template_path)
        
        # Add the template directory to the loader
        self.template_env.loader.searchpath.insert(0, template_dir)
        self.template_name = template_name
        self.slide_template = self.template_env.get_template(template_name)

    def process_markdown(self, markdown, page, config):
        """Process markdown content and replace slides blocks with HTML"""
        self.config = config
        self.page = page  # Store the page object for path resolution

        def replace_slides(match):
            try:
                slide_config = yaml.safe_load(match.group(1))
                if not all(key in slide_config for key in ["title", "url_stub", "nav"]):
                    raise ValueError("Missing required fields in slides configuration")

                slides = self._load_slides(slide_config["nav"])
                html = self._generate_slides_html(slide_config, slides)
                return html
            except Exception as e:
                return f'<div class="slides-error">Error processing slides: {str(e)}</div>'

        return self.slides_pattern.sub(replace_slides, markdown)

    def _load_slides(self, nav_paths):
        """Load and process slide content"""
        slides = []
        docs_dir = self.config["docs_dir"]
        site_dir = self.config["site_dir"]
        current_file_dir = os.path.dirname(os.path.join(docs_dir, self.page.file.src_path))

        for path in nav_paths:
            try:
                # Try multiple path resolutions in order:
                possible_paths = [
                    os.path.join(current_file_dir, path),  # Relative to current file
                    os.path.join(docs_dir, path),          # Relative to docs root
                    os.path.join(docs_dir, "slides", path) # Legacy support for slides/ directory
                ]

                md_path = None
                for possible_path in possible_paths:
                    if os.path.exists(possible_path):
                        md_path = possible_path
                        break

                if md_path is None:
                    raise FileNotFoundError(
                        f"Could not find slide file '{path}'. Tried:\n" +
                        "\n".join(f"- {p}" for p in possible_paths)
                    )

                with open(md_path, "r", encoding="utf-8") as f:
                    content = f.read()

                # Process markdown with specific extensions
                md = Markdown(
                    extensions=[
                        "meta",
                        "tables",
                        "fenced_code",
                        "attr_list",
                        "codehilite",
                        "pymdownx.superfences",
                    ]
                )
                html_content = md.convert(content.strip())

                # Process Mermaid blocks
                if '```mermaid' in content:
                    # First pattern for the main content
                    html_content = re.sub(
                        r'<div class="highlight"><pre><span></span><code>graph',
                        r'<pre class="mermaid"><code>graph',
                        html_content
                    )
                    # Clean up the closing tags
                    html_content = html_content.replace(
                        '</code></pre></div>',
                        '</code></pre>'
                    )
                    # Also handle any overview/duplicate blocks
                    html_content = html_content.replace(
                        '<div class="highlight"><pre>',
                        '<pre class="mermaid">'
                    ).replace(
                        '</pre></div>',
                        '</pre>'
                    )

                title = self._extract_slide_title(content)
                
                slides.append({
                    "content": html_content,
                    "title": title,
                })

            except Exception as e:
                print(f"Error processing slide {path}: {str(e)}")
                continue

        return slides

    def write_files(self):
        """Write all collected files"""
        for file_info in self.files_to_write:
            os.makedirs(os.path.dirname(file_info["path"]), exist_ok=True)
            with open(file_info["path"], "w", encoding="utf-8") as f:
                f.write(file_info["content"])
        self.files_to_write = []  # Clear the list after writing

    def _extract_slide_title(self, content):
        """Extract the title from slide content"""
        # Look for first heading in the markdown
        match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
        if match:
            return match.group(1)
        return "Untitled Slide"

    def _generate_slides_html(self, config, slides):
        """Generate the slides container with divs"""
        style = f"""
            --slide-padding: {self.config.get('padding', '64px')};
            --slide-max-width: {self.config.get('max_width', '1200px')};
            --slide-aspect-ratio: {self.config.get('aspect_ratio', '16/9')};
            --slide-font-size: {self.config.get('font_size', '24px')};
        """

        html = f'<div class="slides-deck" style="{style}">'
        html += '<div class="slides-viewport">'

        # Main slides as divs
        for i, slide in enumerate(slides):
            display = 'block' if i == 0 else 'none'
            html += f'<div class="slide" data-index="{i}" style="display: {display}">'
            html += slide['content']
            html += '</div>'
        html += '</div>'

        # Overview grid
        html += '<div class="slides-overview">'
        html += '<button class="overview-close" title="Close overview (Esc)">×</button>'
        for i, slide in enumerate(slides):
            html += f'<div class="overview-slide" data-index="{i}">'
            html += slide['content']  # Use content directly instead of iframe
            html += f'<span class="overview-number">{i + 1}</span>'
            html += '</div>'
        html += '</div>'

        # Controls (unchanged)
        html += '<div class="slides-controls">'
        html += '<div class="nav-controls">'
        html += '<button class="prev-slide" title="Previous (← Left arrow)">←</button>'
        html += f'<span class="slide-progress">1 / {len(slides)}</span>'
        html += '<button class="next-slide" title="Next (→ Right arrow)">→</button>'
        html += '</div>'
        html += '<div class="button-group">'
        html += '<button class="overview-toggle" title="Toggle overview (O)">⊞</button>'
        html += '<button class="fullscreen-toggle" title="Toggle fullscreen">⛶</button>'
        html += '</div>'
        html += '</div>'

        # Mobile controls (unchanged)
        html += '<div class="mobile-nav">'
        html += '<button class="mobile-prev">←</button>'
        html += '<button class="mobile-overview">⊞</button>'
        html += '<button class="mobile-next">→</button>'
        html += '</div>'
        html += '<button class="mobile-close">×</button>'

        html += '</div>'
        return html

    def on_page_content(self, html, page, config, files):
        """Process the entire page content at once"""
        try:
            if not '```slides' in html:
                return html

            # Extract slide content
            slides_match = re.search(r'```slides(.*?)```', html, re.DOTALL)
            if not slides_match:
                return html

            # Process all slides in one go
            slides_config = yaml.safe_load(slides_match.group(1))
            slides_html = self._process_slides(slides_config, config)
            
            # Replace the slides block with processed HTML
            return html.replace(slides_match.group(0), slides_html)
        except Exception as e:
            print(f"Error processing slides: {str(e)}")
            return html
