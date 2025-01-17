# Usage Guide

## Basic Usage

Create a slide deck using the `slides` fence block:

```yaml
slides
    title: My Presentation
    url_stub: my-pres
    nav:
        - slides/presentation/*.md
```

## Slide Content

Each slide is a separate markdown file. Example slide:

```markdown
# Slide Title

- Bullet point 1
- Bullet point 2

## Subheading

More content here...
```

## Navigation

- Use left/right arrow keys
- Click navigation buttons
- Press 'F' for fullscreen
- Use URL with #slide-number 