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
        # Default configuration
        self.config = {
            'padding': '64px',
            'max_width': '1200px',
            'aspect_ratio': '16/9',
            'font_size': '24px'
        }

    def set_config(self, config):
        # Update defaults with any provided config values
        if config:
            self.config.update(config)

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
                html = self._generate_slides_html(slide_config, slides)
                # print("Generated HTML for slides:", html[:500])  # Print first 500 chars
                return html
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
                # Get absolute path to markdown file
                md_path = os.path.join(docs_dir, 'slides', path)
                if not os.path.exists(md_path):
                    md_path = os.path.join(docs_dir, path)
                
                with open(md_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Process markdown with specific extensions
                md = Markdown(extensions=[
                    'meta',
                    'tables',
                    'fenced_code',
                    'attr_list',
                    'codehilite'  # Add syntax highlighting support
                ])
                html_content = md.convert(content.strip())
                
                # Ensure code blocks have proper language classes
                html_content = html_content.replace('<pre><code>', '<pre><code class="hljs">')
                
                # Ensure no wrapping divs are added
                html_content = html_content.replace('<div class="markdown">', '').replace('</div>', '')
                
                title = self._extract_slide_title(content)

                # Generate HTML file path
                html_path = os.path.splitext(path)[0] + '.html'
                abs_html_path = os.path.join(site_dir, 'slides', html_path)
                
                # Create slide HTML
                slide_html = self.slide_template.render(
                    content=html_content,
                    title=title
                )

                self.files_to_write.append({
                    'path': abs_html_path,
                    'content': slide_html
                })

                # Calculate relative path
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
        style = f'''
            --slide-padding: {self.config.get('padding', '64px')};
            --slide-max-width: {self.config.get('max_width', '1200px')};
            --slide-aspect-ratio: {self.config.get('aspect_ratio', '16/9')};
            --slide-font-size: {self.config.get('font_size', '24px')};
        '''
        
        html = f'<div class="slides-deck" style="{style}">'
        html += '<div class="slides-viewport">'
        
        # Add slides
        for i, slide in enumerate(slides):
            display = 'block' if i == 0 else 'none'
            html += f'<iframe class="slide" src="{slide["html_path"]}" style="display: {display}"></iframe>'
        html += '</div>'
        
        # Add controls with tooltips and fullscreen button
        html += '<div class="slides-controls">'
        html += '<div class="nav-controls">'
        html += '<button class="prev-slide" title="Previous (← Left arrow)">←</button>'
        html += f'<span class="slide-progress">1 / {len(slides)}</span>'
        html += '<button class="next-slide" title="Next (→ Right arrow)">→</button>'
        html += '</div>'
        html += '<button class="fullscreen-toggle" title="Toggle fullscreen (F)">⛶</button>'
        html += '</div>'
        
        html += '</div>'
        return html 