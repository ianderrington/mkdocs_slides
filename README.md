# MkDocs Slides Plugin

A plugin for MkDocs that enables beautiful slide presentations within your documentation.

## Installation

```bash
pip install mkdocs-slides
```

## Usage

Add the plugin to your `mkdocs.yml`:

```yaml
plugins:
  - slides
```

Create a slide deck in your markdown:

```yaml
slides
    title: My Presentation
    url_stub: my-pres
    nav:
        - slides/presentation/*.md
```

For full documentation, visit [the plugin documentation](https://ianderrington.github.io/mkdocs_slides/).

## License

This project is licensed under the MIT License - see the LICENSE file for details. 
