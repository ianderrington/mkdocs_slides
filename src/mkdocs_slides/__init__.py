from mkdocs.plugins import BasePlugin
import os
from mkdocs.structure.files import File
from .slide_parser import SlideParser

class SlidesPlugin(BasePlugin):
    def __init__(self):
        super().__init__()
        self.parser = SlideParser()
        
    def on_files(self, files, config):
        """Register static assets"""
        # Get the actual path to static files
        static_dir = os.path.join(os.path.dirname(__file__), 'static')
        
        # Add CSS file
        files.append(File(
            path='slides.css',  # Just the filename
            src_dir=os.path.join(static_dir, 'css'),  # Full path to css directory
            dest_dir=os.path.join(config['site_dir'], 'assets', 'slides', 'css'),
            use_directory_urls=False
        ))
        
        # Add JS file
        files.append(File(
            path='slides.js',  # Just the filename
            src_dir=os.path.join(static_dir, 'js'),  # Full path to js directory
            dest_dir=os.path.join(config['site_dir'], 'assets', 'slides', 'js'),
            use_directory_urls=False
        ))
        
        return files

    def on_page_markdown(self, markdown, page, config, files):
        """Process the markdown content and replace slides blocks with HTML"""
        try:
            processed_markdown = self.parser.process_markdown(
                markdown=markdown,
                page=page,
                config=config
            )
            
            if '```slides' in markdown:
                # Write slide files
                self.parser.write_files()
                
                # Add CSS/JS
                page.head_extra = [
                    '<link rel="stylesheet" href="/assets/slides/css/slides.css">',
                    '<script src="/assets/slides/js/slides.js"></script>'
                ]
            return processed_markdown
        except Exception as e:
            print(f"Error processing slides in {page.file.src_path}: {str(e)}")
            return markdown

def get_plugin():
    return SlidesPlugin

# Make sure these are directly importable
__all__ = ['SlidesPlugin', 'get_plugin'] 