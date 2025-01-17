
# MkDocs Slides Plugin Build Plan

## Overview
A MkDocs plugin that enables embedding slide presentations within documentation pages, with support for multiple slide decks per page, fullscreen viewing, and URL-based navigation.

## Requirements

### Core Functionality
1. Parse slide deck definitions in markdown using the `slides` fence block
2. Support multiple slide decks per page with unique URL stubs
3. Load slides from specified markdown files
4. Support glob patterns for slide paths (e.g., `slidepathC/*.md`)
5. Generate unique URLs for each slide using the format `<baseurl>/<url_stub>#<slide_title>`
6. Provide navigation between slides (left/right arrows)
7. Enable fullscreen/lightbox mode
8. Validate URL stubs to prevent duplicates within the same page

### Syntax Example
```yaml
slides
    title: The title of the slides
    url_stub: the_title_of_the_slides
    nav:  
        - slidepathA/slide1.md
        - slidepathB/slide2.md
        - slidepathC/*.md
        
```

## Implementation Plan

### 1. Plugin Structure
```
mkdocs_slides/
├── __init__.py
├── plugin.py
├── renderer.py
├── slide_parser.py
├── static/
│   ├── css/
│   │   └── slides.css
│   └── js/
│       └── slides.js
└── templates/
    └── slides.html
```

### 2. Core Components

#### Plugin Class (plugin.py)
- Register as MkDocs plugin
- Hook into `on_page_markdown`
- Handle asset injection
- Manage configuration

#### Slide Parser (slide_parser.py)
- Parse `slides` fence blocks
- Validate URL stubs
- Process glob patterns
- Load and parse markdown files
- Generate slide metadata

#### Renderer (renderer.py)
- Convert parsed slides to HTML
- Handle template rendering
- Generate navigation elements

### 3. Frontend Components

#### HTML Template (slides.html)
- Responsive slide container
- Navigation controls
- Fullscreen button
- Progress indicator

#### JavaScript (slides.js)
- Slide navigation logic
- Keyboard controls (left/right arrows)
- Fullscreen toggle
- URL hash management
- Touch support for mobile

#### CSS (slides.css)
- Slide styling
- Transitions
- Responsive design
- Fullscreen mode

## Development Phases

### Phase 1: Core Parser
- Implement basic plugin structure
- Create slide parser
- Handle markdown file loading
- Basic validation

### Phase 2: Rendering
- Develop HTML template
- Implement basic styling
- Create slide container

### Phase 3: Navigation
- Add navigation controls
- Implement keyboard shortcuts
- URL hash management
- Touch controls

### Phase 4: Enhanced Features
- Fullscreen mode
- Transitions
- Progress indicator
- Multiple slide deck support

### Phase 5: Testing & Documentation
- Unit tests
- Integration tests
- Usage documentation
- Example implementations

## Testing Strategy

### Unit Tests
- Parser validation
- URL stub uniqueness
- Glob pattern processing
- Markdown conversion

### Integration Tests
- Multiple slide decks
- Asset injection
- URL functionality
- Navigation features

### Browser Testing
- Cross-browser compatibility
- Mobile responsiveness
- Touch interactions
- Keyboard navigation

## Documentation Requirements

### User Guide
- Installation instructions
- Configuration options
- Syntax reference
- Examples

### Developer Guide
- Architecture overview
- Component documentation
- Contributing guidelines
- Testing procedures

## Future Enhancements
- Slide transitions customization
- Custom themes support
- Presenter notes
- PDF export
- Remote control functionality
