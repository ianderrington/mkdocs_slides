# MkDocs Slides Plugin

A powerful way to embed beautiful slide presentations within your MkDocs documentation.

## Features

- Beautiful slide decks embedded directly in your documentation
- Full markdown support with syntax highlighting
- Keyboard navigation and fullscreen mode
- Multiple slide decks per page
- Support for glob patterns when including slides
- Seamless integration with MkDocs

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

Each slide is a separate markdown file. Example slide:

`slide1.md`

```markdown
# Slide Title

- Bullet point 1
- Bullet point 2

## Subheading

More content here...
```


4. Add the slide deck to your documentation (remove the @)

```markdown
```@slides
title: My First Slide Deck
url_stub: unique-url-id
nav:
        - slides/deck1/*.md
```
````

Check out the [Demo](slides/slides_demo.md) to see it in action! 