import re
import yaml
import glob
import os
from pathlib import Path
from markdown import Markdown
import jinja2

class SlideParser:
    def __init__(self):
        self.slides_pattern = re.compile(r'```slides\s*(.*?)```', re.DOTALL)
        self.template_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(
                os.path.join(os.path.dirname(__file__), 'templates')
            )
        )
        self.slide_template = self.template_env.get_template('slide_template.html')
        self.files_to_write = []  # Store files that need to be written

    def process_markdown(self, markdown, page, config):
        """Process markdown content and replace slides blocks with HTML"""
        self.config = config
        self.page = page
        
        def replace_slides(match):
            try:
                slide_config = yaml.safe_load(match.group(1))
                if not all(key in slide_config for key in ['title', 'url_stub', 'nav']):
                    raise ValueError("Missing required fields in slides configuration")
                
                slides = self._load_slides(slide_config['nav'])
                return self._generate_slides_html(slide_config, slides)
            except Exception as e:
                return f'<div class="slides-error">Error processing slides: {str(e)}</div>'
        
        return self.slides_pattern.sub(replace_slides, markdown)

    def _load_slides(self, nav_paths):
        """Load and process slide content"""
        slides = []
        docs_dir = self.config['docs_dir']
        site_dir = self.config['site_dir']

        for path in nav_paths:
            try:
                # Get absolute path to markdown file - look in slides directory
                md_path = os.path.join(docs_dir, 'slides', path)
                if not os.path.exists(md_path):
                    # Try without slides prefix in case path is already complete
                    md_path = os.path.join(docs_dir, path)
                
                with open(md_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Process markdown
                md = Markdown(extensions=self.config.get('markdown_extensions', []))
                html_content = md.convert(content.strip())
                title = self._extract_slide_title(content)

                # Generate HTML file path preserving directory structure
                html_path = os.path.splitext(path)[0] + '.html'
                abs_html_path = os.path.join(site_dir, 'slides', html_path)
                
                # Create slide HTML
                slide_html = self.slide_template.render(
                    content=html_content,
                    title=title
                )

                # Store file info for writing
                self.files_to_write.append({
                    'path': abs_html_path,
                    'content': slide_html
                })

                # Calculate relative path from current page to slide
                page_dir = os.path.dirname(self.page.url)
                rel_path = os.path.relpath(
                    os.path.join('slides', html_path),
                    page_dir
                )

                slides.append({
                    'html_path': rel_path,
                    'title': title
                })

            except Exception as e:
                raise ValueError(f"Error processing slide {path}: {str(e)}")

        return slides

    def write_files(self):
        """Write all collected files"""
        for file_info in self.files_to_write:
            os.makedirs(os.path.dirname(file_info['path']), exist_ok=True)
            with open(file_info['path'], 'w', encoding='utf-8') as f:
                f.write(file_info['content'])
        self.files_to_write = []  # Clear the list after writing

    def _extract_slide_title(self, content):
        """Extract the title from slide content"""
        # Look for first heading in the markdown
        match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if match:
            return match.group(1)
        return "Untitled Slide"

    def _generate_slides_html(self, config, slides):
        """Generate the slides container with iframes"""
        html = f'<div class="slides-container" data-url-stub="{config["url_stub"]}">'
        html += f'<h2 class="slides-title">{config["title"]}</h2>'
        html += '<div class="slides-deck">'
        
        # Add iframe container
        html += '<div class="slides-viewport">'
        for i, slide in enumerate(slides):
            html += f'<iframe class="slide" id="{config["url_stub"]}-slide-{i+1}" src="{slide["html_path"]}" frameborder="0"></iframe>'
        html += '</div>'
        
        # Add controls
        html += '<div class="slides-controls">'
        html += '<button class="prev-slide" title="Previous slide">←</button>'
        html += '<span class="slide-progress"></span>'
        html += '<button class="next-slide" title="Next slide">→</button>'
        html += '<button class="fullscreen" title="Toggle fullscreen">⛶</button>'
        html += '</div>'
        
        html += '</div></div>'
        return html 