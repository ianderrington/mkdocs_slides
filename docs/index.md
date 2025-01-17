# MkDocs Slides Plugin

A plugin for MkDocs that enables beautiful slide presentations within your documentation.

## Features

- Embed slide decks directly in your documentation
- Full markdown support for slides
- Navigation with keyboard arrows or buttons
- Fullscreen presentation mode
- URL-based navigation to specific slides
- Multiple slide decks per page
- Support for glob patterns when including slides

## Quick Start

1. Install the plugin:
```bash
pip install mkdocs-slides
```

2. Add it to your mkdocs.yml:
```yaml
plugins:
  - slides
```

3. Create your first slide deck:
```yaml
slides
    title: My First Slide Deck
    url_stub: first-deck
    nav:
        - slides/deck1/*.md
```

Check out the [Demo](slides/slides_demo.md) to see it in action! 